"""
Modèles de l'app categories.

Un seul modèle : Categorie.

Une catégorie est un regroupement transversal, identifié par son
`type` (projet, laboratoire, article, etude_de_cas). Cela évite de
créer 4 tables distinctes quasi-identiques.

Règles de slug (validées Phase 2) :
- Pré-rempli automatiquement dans l'admin depuis `nom`
- Modifiable manuellement
- Fallback serveur si vide
- Unique par couple (type, slug)
- 200 caractères max
"""

from django.db import models
from django.utils.text import slugify


class Categorie(models.Model):
    """Catégorie d'un contenu, typée par domaine fonctionnel."""

    class TypeChoices(models.TextChoices):
        PROJET = "projet", "Projet"
        LABORATOIRE = "laboratoire", "Laboratoire"
        ARTICLE = "article", "Article"
        ETUDE_DE_CAS = "etude_de_cas", "Étude de cas"

    nom = models.CharField(max_length=100, verbose_name="Nom")
    slug = models.SlugField(
        max_length=200,
        blank=True,
        verbose_name="Slug",
        help_text="Laisser vide pour génération automatique depuis le nom.",
    )
    type = models.CharField(
        max_length=20,
        choices=TypeChoices.choices,
        verbose_name="Type",
        help_text="Domaine fonctionnel de cette catégorie.",
    )
    description = models.TextField(
        blank=True, verbose_name="Description"
    )
    ordre = models.PositiveIntegerField(default=0, verbose_name="Ordre")

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ["type", "ordre", "nom"]
        constraints = [
            models.UniqueConstraint(
                fields=["type", "slug"],
                name="unique_slug_par_type_categorie",
            ),
        ]

    def __str__(self) -> str:
        return f"[{self.get_type_display()}] {self.nom}"

    def save(self, *args, **kwargs):
        """Génère le slug si vide, en garantissant l'unicité par type."""
        if not self.slug:
            base = slugify(self.nom)[:200] or "sans-titre"
            slug = base
            n = 2
            while (
                type(self)
                .objects.filter(type=self.type, slug=slug)
                .exclude(pk=self.pk)
                .exists()
            ):
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)