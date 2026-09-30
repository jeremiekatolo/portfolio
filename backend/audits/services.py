"""
Service utilitaire pour créer des entrées d'audit.

Usage type depuis une vue :
    from audits.services import journaliser
    journaliser(
        utilisateur=request.user,
        action=AuditLog.ActionChoices.CONTENT_PUBLISHED,
        content_object=projet,
        request=request,
        metadonnees={"ancien_statut": "brouillon"},
    )
"""

from django.contrib.contenttypes.models import ContentType

from .models import AuditLog


def journaliser(
    *,
    action: str,
    utilisateur=None,
    content_object=None,
    request=None,
    resultat: str = AuditLog.ResultatChoices.SUCCES,
    metadonnees: dict | None = None,
) -> AuditLog:
    """
    Crée une entrée d'audit.

    Ne lève jamais d'exception : si la journalisation échoue, elle est
    silencieusement ignorée pour ne pas casser l'action métier.
    """
    try:
        content_type = None
        object_id = None
        if content_object is not None and content_object.pk:
            content_type = ContentType.objects.get_for_model(content_object)
            object_id = content_object.pk

        ip_hash = ""
        if request is not None:
            xff = request.META.get("HTTP_X_FORWARDED_FOR", "")
            ip = xff.split(",")[0].strip() if xff else request.META.get("REMOTE_ADDR", "")
            ip_hash = AuditLog.hasher_ip(ip)

        return AuditLog.objects.create(
            utilisateur=utilisateur if (utilisateur and utilisateur.is_authenticated) else None,
            action=action,
            content_type=content_type,
            object_id=object_id,
            ip_hash=ip_hash,
            resultat=resultat,
            metadonnees=metadonnees or {},
        )
    except Exception:
        # Règle : la journalisation ne doit jamais casser l'action métier.
        return None  # type: ignore[return-value]