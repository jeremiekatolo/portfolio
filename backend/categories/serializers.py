"""
Serializers DRF pour l'app categories.

- CategorieSerializer : CRUD complet sur les catégories.
  Le champ `slug` est optionnel en écriture (généré par le modèle si vide).
  La validation d'unicité (type, slug) est faite manuellement, car DRF
  auto-génère un UniqueTogetherValidator qui exigerait `slug` même quand
  il est optionnel.
"""

from rest_framework import serializers

from .models import Categorie


class CategorieSerializer(serializers.ModelSerializer):
    """
    Serializer Categorie avec slug optionnel.

    Particularités :
    - `slug` est optionnel : s'il est omis, le modèle en génère un.
    - La contrainte d'unicité (type, slug) est vérifiée manuellement,
      uniquement si un slug explicite est fourni.
    """

    type_display = serializers.CharField(source="get_type_display", read_only=True)
    slug = serializers.SlugField(
        required=False, allow_blank=True, max_length=200
    )

    class Meta:
        model = Categorie
        fields = (
            "id",
            "nom",
            "slug",
            "type",
            "type_display",
            "description",
            "ordre",
        )
        read_only_fields = ("id",)
        # Désactive les validateurs auto-générés par DRF (UniqueTogetherValidator).
        # La contrainte DB reste active : elle protège contre les doublons
        # en cas de contournement du serializer.
        validators = []

    def validate(self, attrs):
        """
        Vérifie manuellement l'unicité de (type, slug) si un slug est fourni.

        Si le slug est vide, la validation est déléguée à `Categorie.save()`,
        qui génère un slug unique automatiquement.
        """
        type_val = attrs.get("type", getattr(self.instance, "type", None))
        slug = attrs.get("slug")

        # Si le slug est vide, on laisse `save()` gérer la génération.
        if not slug:
            return attrs

        # Vérifie l'unicité (type, slug) en excluant l'instance en cours de modif.
        qs = Categorie.objects.filter(type=type_val, slug=slug)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                {
                    "slug": (
                        "Une catégorie avec ce slug existe déjà pour ce type. "
                        "Choisissez un autre slug ou laissez-le vide "
                        "pour une génération automatique."
                    )
                }
            )
        return attrs