"""
Services métier pour l'app laboratoires.

Contient la logique de transition de statut (workflow de publication).
Chaque fonction :
- vérifie la transition
- met à jour le statut
- journalise l'action dans AuditLog
- retourne l'instance mise à jour
"""

from audits.models import AuditLog
from audits.services import journaliser
from core.exceptions import ActionNonAutorisee, TransitionInvalide
from django.contrib.auth import get_user_model

from .models import Laboratoire

Utilisateur = get_user_model()


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


def soumettre(instance: Laboratoire, *, user, request=None) -> Laboratoire:
    """Brouillon → En révision. Éditeur ou admin."""
    if not _est_editeur_ou_admin(user):
        raise ActionNonAutorisee(
            "Seul un éditeur ou un administrateur peut soumettre un laboratoire."
        )
    if instance.statut != Laboratoire.StatutChoices.BROUILLON:
        raise TransitionInvalide(
            f"Impossible de soumettre un laboratoire au statut `{instance.get_statut_display()}`."
        )

    ancien = instance.statut
    instance.statut = Laboratoire.StatutChoices.EN_REVISION
    instance.save(update_fields=["statut", "date_modification"])

    journaliser(
        utilisateur=user,
        action=AuditLog.ActionChoices.CONTENT_UPDATED,
        content_object=instance,
        request=request,
        metadonnees={"transition": "soumettre", "ancien": ancien, "nouveau": instance.statut},
    )
    return instance


def valider(instance: Laboratoire, *, user, request=None) -> Laboratoire:
    """En révision → Validé. Admin uniquement."""
    if not _est_admin(user):
        raise ActionNonAutorisee(
            "Seul un administrateur peut valider un laboratoire."
        )
    if instance.statut != Laboratoire.StatutChoices.EN_REVISION:
        raise TransitionInvalide(
            f"Impossible de valider un laboratoire au statut `{instance.get_statut_display()}`."
        )

    ancien = instance.statut
    instance.statut = Laboratoire.StatutChoices.VALIDE
    instance.save(update_fields=["statut", "date_modification"])

    journaliser(
        utilisateur=user,
        action=AuditLog.ActionChoices.CONTENT_UPDATED,
        content_object=instance,
        request=request,
        metadonnees={"transition": "valider", "ancien": ancien, "nouveau": instance.statut},
    )
    return instance


def publier(instance: Laboratoire, *, user, request=None) -> Laboratoire:
    """Brouillon / En révision / Validé → Publié. Admin uniquement."""
    if not _est_admin(user):
        raise ActionNonAutorisee(
            "Seul un administrateur peut publier un laboratoire."
        )
    if instance.statut not in (
        Laboratoire.StatutChoices.BROUILLON,
        Laboratoire.StatutChoices.EN_REVISION,
        Laboratoire.StatutChoices.VALIDE,
    ):
        raise TransitionInvalide(
            f"Impossible de publier un laboratoire au statut `{instance.get_statut_display()}`."
        )

    ancien = instance.statut
    instance.statut = Laboratoire.StatutChoices.PUBLIE
    instance.save(update_fields=["statut", "date_modification"])

    journaliser(
        utilisateur=user,
        action=AuditLog.ActionChoices.CONTENT_PUBLISHED,
        content_object=instance,
        request=request,
        metadonnees={"transition": "publier", "ancien": ancien, "nouveau": instance.statut},
    )
    return instance


def depublier(instance: Laboratoire, *, user, request=None) -> Laboratoire:
    """Publié → Brouillon. Admin uniquement."""
    if not _est_admin(user):
        raise ActionNonAutorisee(
            "Seul un administrateur peut dépublier un laboratoire."
        )
    if instance.statut != Laboratoire.StatutChoices.PUBLIE:
        raise TransitionInvalide(
            f"Impossible de dépublier un laboratoire au statut `{instance.get_statut_display()}`."
        )

    ancien = instance.statut
    instance.statut = Laboratoire.StatutChoices.BROUILLON
    instance.save(update_fields=["statut", "date_modification"])

    journaliser(
        utilisateur=user,
        action=AuditLog.ActionChoices.CONTENT_UNPUBLISHED,
        content_object=instance,
        request=request,
        metadonnees={"transition": "depublier", "ancien": ancien, "nouveau": instance.statut},
    )
    return instance


def archiver(instance: Laboratoire, *, user, request=None) -> Laboratoire:
    """Validé / Publié → Archivé. Admin uniquement. État terminal."""
    if not _est_admin(user):
        raise ActionNonAutorisee(
            "Seul un administrateur peut archiver un laboratoire."
        )
    if instance.statut not in (
        Laboratoire.StatutChoices.VALIDE,
        Laboratoire.StatutChoices.PUBLIE,
    ):
        raise TransitionInvalide(
            f"Impossible d'archiver un laboratoire au statut `{instance.get_statut_display()}`."
        )

    ancien = instance.statut
    instance.statut = Laboratoire.StatutChoices.ARCHIVE
    instance.save(update_fields=["statut", "date_modification"])

    journaliser(
        utilisateur=user,
        action=AuditLog.ActionChoices.CONTENT_ARCHIVED,
        content_object=instance,
        request=request,
        metadonnees={"transition": "archiver", "ancien": ancien, "nouveau": instance.statut},
    )
    return instance