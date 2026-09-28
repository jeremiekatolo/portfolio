"""
Modèles de l'app technologies.

Un seul modèle : Technologie.

Une technologie est un outil, langage, framework, protocole ou
plateforme utilisé dans les projets et les labs.

Règles :
- `nom` unique (pas de slug — non exposé en URL).
- `logo` optionnel (FK vers Media).
- `categorie_tech` : classement interne (backend, frontend, réseau, ...).
"""

from django.db import models


class Technologie(models.Model):
    """Technologie utilisée dans les projets et laboratoires."""

    class CategorieTechChoices(models.TextChoices):
        BACKEND = "backend", "Backend"
        FRONTEND = "frontend", "Frontend"
        DATABASE = "database", "Base de données"
        RESEAU = "reseau", "Réseau"
        SECURITE = "securite", "Sécurité"
        SYSTEME = "systeme", "Système"
        OUTIL = "outil", "Outil"
        AUTRE = "autre", "Autre"

    nom = models.CharField(
        max_length=100, unique=True, verbose_name="Nom"
    )
    categorie_tech = models.CharField(
        max_length=20,
        choices=CategorieTechChoices.choices,
        default=CategorieTechChoices.AUTRE,
        verbose_name="Catégorie technique",
    )
    description = models.TextField(
        blank=True, verbose_name="Description"
    )
    url_officielle = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="URL officielle",
        help_text="Lien vers la documentation ou le site officiel.",
    )
    logo = models.ForeignKey(
        "medias.Media",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="technologies_utilisant",
        verbose_name="Logo",
    )
    ordre = models.PositiveIntegerField(default=0, verbose_name="Ordre")

    class Meta:
        verbose_name = "Technologie"
        verbose_name_plural = "Technologies"
        ordering = ["categorie_tech", "ordre", "nom"]

    def __str__(self) -> str:
        return self.nom