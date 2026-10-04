"""
Utilitaires transverses pour l'app medias.

Fonction principale : `liens_pour(obj)` — retourne les liens externes
liés à un objet quelconque via ContentType.
"""

from django.contrib.contenttypes.models import ContentType

from .models import LienExterne


def liens_pour(obj) -> list[LienExterne]:
    """
    Retourne les liens externes liés à un objet donné.

    Utilise la liaison polymorphe (ContentType + object_id).
    Triés par `ordre` puis par `id`.
    """
    content_type = ContentType.objects.get_for_model(obj)
    return list(
        LienExterne.objects.filter(
            content_type=content_type, object_id=obj.pk
        ).order_by("ordre", "id")
    )