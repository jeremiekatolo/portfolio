"""
Modèle minimal de l'app laboratoires.

Cette version est MINIMALE : elle ne contient que les champs nécessaires
pour que l'app projets puisse poser sa FK. L'app sera complétée à l'Étape G.
"""

from django.db import models
from django.utils.text import slugify


class Laboratoire(models.Model):
    """Laboratoire technique (version minimale pour FK de Projet)."""

    titre = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(
        max_length=200,
        blank=True,
        unique=True,
        verbose_name="Slug",
    )

    class Meta:
        verbose_name = "Laboratoire"
        verbose_name_plural = "Laboratoires"
        ordering = ["titre"]

    def __str__(self) -> str:
        return self.titre

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.titre)[:200] or "sans-titre"
            slug = base
            n = 2
            while (
                type(self).objects.filter(slug=slug).exclude(pk=self.pk).exists()
            ):
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)