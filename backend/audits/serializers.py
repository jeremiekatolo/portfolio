"""
Serializers DRF pour l'app audits.

Lecture seule stricte : aucune création/modification via API.
La création se fait uniquement via `audits.services.journaliser`.
"""

from rest_framework import serializers

from .models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    """Serializer d'une entrée d'audit (lecture seule)."""

    utilisateur_username = serializers.CharField(
        source="utilisateur.username", read_only=True, default=None
    )
    action_display = serializers.CharField(
        source="get_action_display", read_only=True
    )
    resultat_display = serializers.CharField(
        source="get_resultat_display", read_only=True
    )
    content_type_nom = serializers.CharField(
        source="content_type.model", read_only=True, default=None
    )

    class Meta:
        model = AuditLog
        fields = (
            "id",
            "utilisateur",
            "utilisateur_username",
            "action",
            "action_display",
            "content_type",
            "content_type_nom",
            "object_id",
            "date",
            "ip_hash",
            "resultat",
            "resultat_display",
            "metadonnees",
        )
        read_only_fields = fields