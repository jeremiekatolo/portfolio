"""
Services métier pour l'app etudes_de_cas.

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

from .models import EtudeDeCas

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


def soumettre(instance: EtudeDeCas, *, user, request=None) -> EtudeDeCas:
    """Brouillon → En révision. Éditeur ou admin."""
    if not _est_editeur_ou_admin(user):
        raise ActionNonAutorisee(
            "Seul un éditeur ou un administrateur peut soumettre une étude de cas."
        )
    if instance.statut != EtudeDeCas.StatutChoices.BROUILLON:
        raise TransitionInvalide(
            f"Impossible de soumettre une étude de cas au statut `{instance.get_statut_display()}`."
        )

    ancien = instance.statut
    instance.statut = EtudeDeCas.StatutChoices.EN_REVISION
    instance.save(update_fields=["statut", "date_modification"])

    journaliser(
        utilisateur=user,
        action=AuditLog.ActionChoices.CONTENT_UPDATED,
        content_object=instance,
        request=request,
        metadonnees={"transition": "soumettre", "ancien": ancien, "nouveau": instance.statut},
    )
    return instance


def valider(instance: EtudeDeCas, *, user, request=None) -> EtudeDeCas:
    """En révision → Validé. Admin uniquement."""
    if not _est_admin(user):
        raise ActionNonAutorisee(
            "Seul un administrateur peut valider une étude de cas."
        )
    if instance.statut != EtudeDeCas.StatutChoices.EN_REVISION:
        raise TransitionInvalide(
            f"Impossible de valider une étude de cas au statut `{instance.get_statut_display()}`."
        )

    ancien = instance.statut
    instance.statut = EtudeDeCas.StatutChoices.VALIDE
    instance.save(update_fields=["statut", "date_modification"])

    journaliser(
        utilisateur=user,
        action=AuditLog.ActionChoices.CONTENT_UPDATED,
        content_object=instance,
        request=request,
        metadonnees={"transition": "valider", "ancien": ancien, "nouveau": instance.statut},
    )
    return instance


def publier(instance: EtudeDeCas, *, user, request=None) -> EtudeDeCas:
    """Brouillon / En révision / Validé → Publié. Admin uniquement."""
    if not _est_admin(user):
        raise ActionNonAutorisee(
            "Seul un administrateur peut publier une étude de cas."
        )
    if instance.statut not in (
        EtudeDeCas.StatutChoices.BROUILLON,
        EtudeDeCas.StatutChoices.EN_REVISION,
        EtudeDeCas.StatutChoices.VALIDE,
    ):
        raise TransitionInvalide(
            f"Impossible de publier une étude de cas au statut `{instance.get_statut_display()}`."
        )

    ancien = instance.statut
    instance.statut = EtudeDeCas.StatutChoices.PUBLIE
    instance.save(update_fields=["statut", "date_modification"])

    journaliser(
        utilisateur=user,
        action=AuditLog.ActionChoices.CONTENT_PUBLISHED,
        content_object=instance,
        request=request,
        metadonnees={"transition": "publier", "ancien": ancien, "nouveau": instance.statut},
    )
    return instance


def depublier(instance: EtudeDeCas, *, user, request=None) -> EtudeDeCas:
    """Publié → Brouillon. Admin uniquement."""
    if not _est_admin(user):
        raise ActionNonAutorisee(
            "Seul un administrateur peut dépublier une étude de cas."
        )
    if instance.statut != EtudeDeCas.StatutChoices.PUBLIE:
        raise TransitionInvalide(
            f"Impossible de dépublier une étude de cas au statut `{instance.get_statut_display()}`."
        )

    ancien = instance.statut
    instance.statut = EtudeDeCas.StatutChoices.BROUILLON
    instance.save(update_fields=["statut", "date_modification"])

    journaliser(
        utilisateur=user,
        action=AuditLog.ActionChoices.CONTENT_UNPUBLISHED,
        content_object=instance,
        request=request,
        metadonnees={"transition": "depublier", "ancien": ancien, "nouveau": instance.statut},
    )
    return instance


def archiver(instance: EtudeDeCas, *, user, request=None) -> EtudeDeCas:
    """Validé / Publié → Archivé. Admin uniquement. État terminal."""
    if not _est_admin(user):
        raise ActionNonAutorisee(
            "Seul un administrateur peut archiver une étude de cas."
        )
    if instance.statut not in (
        EtudeDeCas.StatutChoices.VALIDE,
        EtudeDeCas.StatutChoices.PUBLIE,
    ):
        raise TransitionInvalide(
            f"Impossible d'archiver une étude de cas au statut `{instance.get_statut_display()}`."
        )

    ancien = instance.statut
    instance.statut = EtudeDeCas.StatutChoices.ARCHIVE
    instance.save(update_fields=["statut", "date_modification"])

    journaliser(
        utilisateur=user,
        action=AuditLog.ActionChoices.CONTENT_ARCHIVED,
        content_object=instance,
        request=request,
        metadonnees={"transition": "archiver", "ancien": ancien, "nouveau": instance.statut},
    )
    return instance