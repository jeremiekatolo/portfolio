"""
Services métier pour l'app projets.

Contient la logique de transition de statut (workflow de publication).
Chaque fonction :
- vérifie la transition
- met à jour le statut
- journalise l'action dans AuditLog
- retourne l'instance mise à jour

Les fonctions lèvent :
- TransitionInvalide si la transition n'est pas autorisée
- ActionNonAutorisee si l'utilisateur n'a pas le rôle requis
"""

from audits.models import AuditLog
from audits.services import journaliser
from core.exceptions import ActionNonAutorisee, TransitionInvalide
from django.contrib.auth import get_user_model

from .models import Projet

Utilisateur = get_user_model()


# ---------------------------------------------------------------------------
# Utilitaires internes
# ---------------------------------------------------------------------------


def _est_admin(user) -> bool:
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return user.role == Utilisateur.Role.ADMINISTRATEUR


def _est_editeur_ou_admin(user) -> bool:
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return user.role in (Utilisateur.Role.EDITEUR, Utilisateur.Role.ADMINISTRATEUR)


# ---------------------------------------------------------------------------
# Transitions de statut
# ---------------------------------------------------------------------------


def soumettre(instance: Projet, *, user, request=None) -> Projet:
    """
    Brouillon → En révision.

    Autorisé à : éditeur, administrateur.
    """
    if not _est_editeur_ou_admin(user):
        raise ActionNonAutorisee(
            "Seul un éditeur ou un administrateur peut soumettre un projet."
        )
    if instance.statut != Projet.StatutChoices.BROUILLON:
        raise TransitionInvalide(
            f"Impossible de soumettre un projet au statut `{instance.get_statut_display()}`."
        )

    ancien = instance.statut
    instance.statut = Projet.StatutChoices.EN_REVISION
    instance.save(update_fields=["statut", "date_modification"])

    journaliser(
        utilisateur=user,
        action=AuditLog.ActionChoices.CONTENT_UPDATED,
        content_object=instance,
        request=request,
        metadonnees={"transition": "soumettre", "ancien": ancien, "nouveau": instance.statut},
    )
    return instance


def valider(instance: Projet, *, user, request=None) -> Projet:
    """
    En révision → Validé.

    Autorisé à : administrateur uniquement.
    """
    if not _est_admin(user):
        raise ActionNonAutorisee(
            "Seul un administrateur peut valider un projet."
        )
    if instance.statut != Projet.StatutChoices.EN_REVISION:
        raise TransitionInvalide(
            f"Impossible de valider un projet au statut `{instance.get_statut_display()}`."
        )

    ancien = instance.statut
    instance.statut = Projet.StatutChoices.VALIDE
    instance.save(update_fields=["statut", "date_modification"])

    journaliser(
        utilisateur=user,
        action=AuditLog.ActionChoices.CONTENT_UPDATED,
        content_object=instance,
        request=request,
        metadonnees={"transition": "valider", "ancien": ancien, "nouveau": instance.statut},
    )
    return instance


def publier(instance: Projet, *, user, request=None) -> Projet:
    """
    Brouillon / En révision / Validé → Publié.

    Autorisé à : administrateur uniquement.
    """
    if not _est_admin(user):
        raise ActionNonAutorisee(
            "Seul un administrateur peut publier un projet."
        )
    if instance.statut not in (
        Projet.StatutChoices.BROUILLON,
        Projet.StatutChoices.EN_REVISION,
        Projet.StatutChoices.VALIDE,
    ):
        raise TransitionInvalide(
            f"Impossible de publier un projet au statut `{instance.get_statut_display()}`."
        )

    ancien = instance.statut
    instance.statut = Projet.StatutChoices.PUBLIE
    instance.save(update_fields=["statut", "date_modification"])

    journaliser(
        utilisateur=user,
        action=AuditLog.ActionChoices.CONTENT_PUBLISHED,
        content_object=instance,
        request=request,
        metadonnees={"transition": "publier", "ancien": ancien, "nouveau": instance.statut},
    )
    return instance


def depublier(instance: Projet, *, user, request=None) -> Projet:
    """
    Publié → Brouillon.

    Autorisé à : administrateur uniquement.
    """
    if not _est_admin(user):
        raise ActionNonAutorisee(
            "Seul un administrateur peut dépublier un projet."
        )
    if instance.statut != Projet.StatutChoices.PUBLIE:
        raise TransitionInvalide(
            f"Impossible de dépublier un projet au statut `{instance.get_statut_display()}`."
        )

    ancien = instance.statut
    instance.statut = Projet.StatutChoices.BROUILLON
    instance.save(update_fields=["statut", "date_modification"])

    journaliser(
        utilisateur=user,
        action=AuditLog.ActionChoices.CONTENT_UNPUBLISHED,
        content_object=instance,
        request=request,
        metadonnees={"transition": "depublier", "ancien": ancien, "nouveau": instance.statut},
    )
    return instance


def archiver(instance: Projet, *, user, request=None) -> Projet:
    """
    Validé / Publié → Archivé.

    Autorisé à : administrateur uniquement.
    L'archive est un état terminal.
    """
    if not _est_admin(user):
        raise ActionNonAutorisee(
            "Seul un administrateur peut archiver un projet."
        )
    if instance.statut not in (
        Projet.StatutChoices.VALIDE,
        Projet.StatutChoices.PUBLIE,
    ):
        raise TransitionInvalide(
            f"Impossible d'archiver un projet au statut `{instance.get_statut_display()}`."
        )

    ancien = instance.statut
    instance.statut = Projet.StatutChoices.ARCHIVE
    instance.save(update_fields=["statut", "date_modification"])

    journaliser(
        utilisateur=user,
        action=AuditLog.ActionChoices.CONTENT_ARCHIVED,
        content_object=instance,
        request=request,
        metadonnees={"transition": "archiver", "ancien": ancien, "nouveau": instance.statut},
    )
    return instance