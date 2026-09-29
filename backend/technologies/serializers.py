"""
Serializers DRF pour l'app technologies.

- TechnologieSerializer : CRUD complet.
  Le champ `logo` est exposé en lecture (URL du fichier) et accepté
  en écriture sous forme d'ID via `logo_id`.
"""

from rest_framework import serializers

from medias.models import Media
from .models import Technologie


class MediaInlineSerializer(serializers.Serializer):
    """Représentation minimale d'un média lié."""

    id = serializers.IntegerField(read_only=True)
    fichier = serializers.FileField(read_only=True)
    alt_text = serializers.CharField(read_only=True)
    type = serializers.CharField(read_only=True)


class TechnologieSerializer(serializers.ModelSerializer):
    """Serializer Technologie avec logo imbriqué en lecture seule."""

    categorie_tech_display = serializers.CharField(
        source="get_categorie_tech_display", read_only=True
    )
    logo = MediaInlineSerializer(read_only=True)
    logo_id = serializers.PrimaryKeyRelatedField(
        source="logo",
        queryset=Media.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Technologie
        fields = (
            "id",
            "nom",
            "categorie_tech",
            "categorie_tech_display",
            "description",
            "url_officielle",
            "logo",
            "logo_id",
            "ordre",
        )
        read_only_fields = ("id",)