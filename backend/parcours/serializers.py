"""
Serializers DRF pour l'app parcours.

- ParcoursSerializer      : lecture d'une entrée du parcours.
- CertificationSerializer : lecture d'une certification.
- Versions écriture : utilisent `profil_id` + `competences_ids` + `badge_id`.
"""

from rest_framework import serializers

from competences.models import Competence
from medias.models import Media
from utilisateurs.models import Profil

from .models import Certification, Parcours


class MediaInlineSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    fichier = serializers.FileField(read_only=True)
    alt_text = serializers.CharField(read_only=True)


class CompetenceInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competence
        fields = ("id", "nom", "domaine")


# ---------------------------------------------------------------------------
# Parcours
# ---------------------------------------------------------------------------


class ParcoursSerializer(serializers.ModelSerializer):
    """Lecture d'une entrée de parcours."""

    type_display = serializers.CharField(source="get_type_display", read_only=True)
    competences = CompetenceInlineSerializer(many=True, read_only=True)
    est_en_cours = serializers.BooleanField(read_only=True)

    class Meta:
        model = Parcours
        fields = (
            "id",
            "profil",
            "titre",
            "type",
            "type_display",
            "organisation",
            "lieu",
            "date_debut",
            "date_fin",
            "description",
            "ordre",
            "competences",
            "est_en_cours",
        )
        read_only_fields = fields


class ParcoursEcritureSerializer(serializers.ModelSerializer):
    """Écriture d'une entrée de parcours."""

    profil_id = serializers.PrimaryKeyRelatedField(
        source="profil",
        queryset=Profil.objects.all(),
    )
    competences_ids = serializers.PrimaryKeyRelatedField(
        source="competences",
        queryset=Competence.objects.all(),
        many=True,
        required=False,
    )

    class Meta:
        model = Parcours
        fields = (
            "id",
            "profil_id",
            "titre",
            "type",
            "organisation",
            "lieu",
            "date_debut",
            "date_fin",
            "description",
            "ordre",
            "competences_ids",
        )
        read_only_fields = ("id",)

    def validate(self, attrs):
        date_debut = attrs.get("date_debut")
        date_fin = attrs.get("date_fin")
        if date_debut and date_fin and date_fin < date_debut:
            raise serializers.ValidationError(
                {"date_fin": "La date de fin ne peut pas être antérieure à la date de début."}
            )
        return attrs

    def create(self, validated_data):
        competences = validated_data.pop("competences", [])
        instance = Parcours.objects.create(**validated_data)
        if competences:
            instance.competences.set(competences)
        return instance

    def update(self, instance, validated_data):
        competences = validated_data.pop("competences", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if competences is not None:
            instance.competences.set(competences)
        return instance


# ---------------------------------------------------------------------------
# Certification
# ---------------------------------------------------------------------------


class CertificationSerializer(serializers.ModelSerializer):
    """Lecture d'une certification."""

    competences = CompetenceInlineSerializer(many=True, read_only=True)
    badge = MediaInlineSerializer(read_only=True)
    est_expiree = serializers.BooleanField(read_only=True)

    class Meta:
        model = Certification
        fields = (
            "id",
            "profil",
            "nom",
            "organisme",
            "date_obtention",
            "date_expiration",
            "identifiant",
            "url_verification",
            "description",
            "badge",
            "ordre",
            "competences",
            "est_expiree",
        )
        read_only_fields = fields


class CertificationEcritureSerializer(serializers.ModelSerializer):
    """Écriture d'une certification."""

    profil_id = serializers.PrimaryKeyRelatedField(
        source="profil",
        queryset=Profil.objects.all(),
    )
    competences_ids = serializers.PrimaryKeyRelatedField(
        source="competences",
        queryset=Competence.objects.all(),
        many=True,
        required=False,
    )
    badge_id = serializers.PrimaryKeyRelatedField(
        source="badge",
        queryset=Media.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Certification
        fields = (
            "id",
            "profil_id",
            "nom",
            "organisme",
            "date_obtention",
            "date_expiration",
            "identifiant",
            "url_verification",
            "description",
            "badge_id",
            "ordre",
            "competences_ids",
        )
        read_only_fields = ("id",)

    def validate(self, attrs):
        date_obtention = attrs.get("date_obtention")
        date_expiration = attrs.get("date_expiration")
        if date_obtention and date_expiration and date_expiration < date_obtention:
            raise serializers.ValidationError(
                {"date_expiration": "La date d'expiration doit être postérieure à la date d'obtention."}
            )
        return attrs

    def create(self, validated_data):
        competences = validated_data.pop("competences", [])
        instance = Certification.objects.create(**validated_data)
        if competences:
            instance.competences.set(competences)
        return instance

    def update(self, instance, validated_data):
        competences = validated_data.pop("competences", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if competences is not None:
            instance.competences.set(competences)
        return instance