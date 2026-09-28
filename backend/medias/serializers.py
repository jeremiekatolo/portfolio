"""
Serializers DRF pour l'app medias.

- MediaSerializer : fichier + métadonnées, URL du fichier exposée en lecture.
- MediaLienSerializer : liaison polymorphe (content_type + object_id).
- LienExterneSerializer : liaison polymorphe vers une URL externe.
"""

from rest_framework import serializers

from .models import LienExterne, Media, MediaLien


class MediaSerializer(serializers.ModelSerializer):
    """Serializer Media avec URL absolue du fichier."""

    fichier_url = serializers.SerializerMethodField()
    uploaded_by_username = serializers.CharField(
        source="uploaded_by.username", read_only=True, default=None
    )
    type_display = serializers.CharField(
        source="get_type_display", read_only=True
    )

    class Meta:
        model = Media
        fields = (
            "id",
            "fichier",
            "fichier_url",
            "nom_original",
            "mime_type",
            "taille",
            "hash_sha256",
            "type",
            "type_display",
            "alt_text",
            "uploaded_by",
            "uploaded_by_username",
            "uploaded_at",
            "est_orphelin",
        )
        read_only_fields = (
            "id",
            "nom_original",
            "mime_type",
            "taille",
            "hash_sha256",
            "uploaded_by",
            "uploaded_at",
            "est_orphelin",
        )

    def get_fichier_url(self, obj):
        """Retourne l'URL absolue du fichier si disponible."""
        if not obj.fichier:
            return None
        request = self.context.get("request")
        url = obj.fichier.url
        if request is not None:
            return request.build_absolute_uri(url)
        return url

    def create(self, validated_data):
        """Associe automatiquement l'utilisateur connecté à l'upload."""
        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            validated_data.setdefault("uploaded_by", request.user)
        return super().create(validated_data)


class MediaLienSerializer(serializers.ModelSerializer):
    """Serializer MediaLien (liaison polymorphe)."""

    media_detail = MediaSerializer(source="media", read_only=True)
    role_display = serializers.CharField(
        source="get_role_display", read_only=True
    )

    class Meta:
        model = MediaLien
        fields = (
            "id",
            "media",
            "media_detail",
            "content_type",
            "object_id",
            "role",
            "role_display",
            "ordre",
            "légende",
        )


class LienExterneSerializer(serializers.ModelSerializer):
    """Serializer LienExterne (liaison polymorphe)."""

    type_display = serializers.CharField(
        source="get_type_display", read_only=True
    )

    class Meta:
        model = LienExterne
        fields = (
            "id",
            "content_type",
            "object_id",
            "type",
            "type_display",
            "url",
            "label",
            "ordre",
        )