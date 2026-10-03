"""
Serializers DRF pour l'app projets.

- ProjetSerializer     : lecture complète (categorie, technologies,
                         competences, liens_externes).
- ProjetEcritureSerializer : écriture (categorie_id, technologies_ids,
                             competences_ids).
"""

from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from categories.models import Categorie
from competences.models import Competence
from etudes_de_cas.models import EtudeDeCas
from laboratoires.models import Laboratoire
from medias.models import LienExterne, Media
from technologies.models import Technologie
from utilisateurs.models import Utilisateur

from .models import Projet


class MediaInlineSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    fichier = serializers.FileField(read_only=True)
    alt_text = serializers.CharField(read_only=True)


class CategorieInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = ("id", "nom", "slug", "type")


class TechnologieInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Technologie
        fields = ("id", "nom", "categorie_tech")


class CompetenceInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competence
        fields = ("id", "nom", "domaine")


class LienExterneInlineSerializer(serializers.ModelSerializer):
    """Lien externe lié à un contenu (GitHub, démo, documentation…)."""

    type_display = serializers.CharField(
        source="get_type_display", read_only=True
    )

    class Meta:
        model = LienExterne
        fields = ("id", "type", "type_display", "url", "label", "ordre")
        read_only_fields = fields


class ProjetSerializer(serializers.ModelSerializer):
    """Serializer de lecture d'un projet."""

    categorie = CategorieInlineSerializer(read_only=True)
    laboratoire_titre = serializers.CharField(
        source="laboratoire.titre", read_only=True, default=None
    )
    etude_de_cas_titre = serializers.CharField(
        source="etude_de_cas.titre", read_only=True, default=None
    )
    technologies = TechnologieInlineSerializer(many=True, read_only=True)
    competences = CompetenceInlineSerializer(many=True, read_only=True)
    liens_externes = serializers.SerializerMethodField()
    auteur_username = serializers.CharField(
        source="auteur.username", read_only=True
    )
    statut_display = serializers.CharField(
        source="get_statut_display", read_only=True
    )
    difficulte_display = serializers.CharField(
        source="get_difficulte_display", read_only=True
    )
    seo_image = MediaInlineSerializer(read_only=True)
    est_public = serializers.BooleanField(read_only=True)

    class Meta:
        model = Projet
        fields = (
            "id",
            "titre",
            "slug",
            "resume",
            "description",
            "probleme",
            "contexte",
            "objectifs",
            "architecture_texte",
            "role",
            "difficulte",
            "difficulte_display",
            "statut",
            "statut_display",
            "publish_at",
            "unpublish_at",
            "date_realisation",
            "duree",
            "resultats",
            "limites",
            "ameliorations_futures",
            "categorie",
            "laboratoire_titre",
            "etude_de_cas_titre",
            "technologies",
            "competences",
            "liens_externes",
            "mis_en_avant",
            "ordre",
            "seo_titre",
            "seo_description",
            "seo_image",
            "auteur_username",
            "date_creation",
            "date_modification",
            "est_public",
        )
        read_only_fields = fields

    def get_liens_externes(self, obj):
        """
        Retourne les liens externes liés à ce projet via ContentType.

        Les liens sont triés par `ordre`, puis par `id`.
        """
        content_type = ContentType.objects.get_for_model(obj)
        liens = LienExterne.objects.filter(
            content_type=content_type, object_id=obj.pk
        ).order_by("ordre", "id")
        return LienExterneInlineSerializer(liens, many=True).data


class ProjetEcritureSerializer(serializers.ModelSerializer):
    """Serializer d'écriture d'un projet."""

    categorie_id = serializers.PrimaryKeyRelatedField(
        source="categorie",
        queryset=Categorie.objects.all(),
    )
    laboratoire_id = serializers.PrimaryKeyRelatedField(
        source="laboratoire",
        queryset=Laboratoire.objects.all(),
        required=False,
        allow_null=True,
    )
    etude_de_cas_id = serializers.PrimaryKeyRelatedField(
        source="etude_de_cas",
        queryset=EtudeDeCas.objects.all(),
        required=False,
        allow_null=True,
    )
    technologies_ids = serializers.PrimaryKeyRelatedField(
        source="technologies",
        queryset=Technologie.objects.all(),
        many=True,
        required=False,
    )
    competences_ids = serializers.PrimaryKeyRelatedField(
        source="competences",
        queryset=Competence.objects.all(),
        many=True,
        required=False,
    )
    seo_image_id = serializers.PrimaryKeyRelatedField(
        source="seo_image",
        queryset=Media.objects.all(),
        required=False,
        allow_null=True,
    )
    auteur_id = serializers.PrimaryKeyRelatedField(
        source="auteur",
        queryset=Utilisateur.objects.all(),
        required=False,
    )

    class Meta:
        model = Projet
        fields = (
            "id",
            "titre",
            "slug",
            "resume",
            "description",
            "probleme",
            "contexte",
            "objectifs",
            "architecture_texte",
            "role",
            "difficulte",
            "statut",
            "publish_at",
            "unpublish_at",
            "date_realisation",
            "duree",
            "resultats",
            "limites",
            "ameliorations_futures",
            "categorie_id",
            "laboratoire_id",
            "etude_de_cas_id",
            "technologies_ids",
            "competences_ids",
            "mis_en_avant",
            "ordre",
            "seo_titre",
            "seo_description",
            "seo_image_id",
            "auteur_id",
        )
        read_only_fields = ("id",)

    def validate(self, attrs):
        slug = attrs.get("slug")
        if slug:
            qs = Projet.objects.filter(slug=slug)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError(
                    {"slug": "Ce slug est déjà utilisé par un autre projet."}
                )
        return attrs

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            validated_data.setdefault("auteur", request.user)
        technologies = validated_data.pop("technologies", [])
        competences = validated_data.pop("competences", [])
        instance = Projet.objects.create(**validated_data)
        if technologies:
            instance.technologies.set(technologies)
        if competences:
            instance.competences.set(competences)
        return instance

    def update(self, instance, validated_data):
        technologies = validated_data.pop("technologies", None)
        competences = validated_data.pop("competences", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if technologies is not None:
            instance.technologies.set(technologies)
        if competences is not None:
            instance.competences.set(competences)
        return instance