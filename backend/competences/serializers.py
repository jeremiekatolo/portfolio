"""
Serializers DRF pour l'app competences.

- CompetenceSerializer : CRUD complet.
  Aucun champ de type `pourcentage` ou `niveau` (règle métier stricte).
"""

from rest_framework import serializers

from .models import Competence


class CompetenceSerializer(serializers.ModelSerializer):
    """Serializer Competence avec domaine_display."""

    domaine_display = serializers.CharField(
        source="get_domaine_display", read_only=True
    )

    class Meta:
        model = Competence
        fields = (
            "id",
            "nom",
            "domaine",
            "domaine_display",
            "description",
            "ordre",
        )
        read_only_fields = ("id",)