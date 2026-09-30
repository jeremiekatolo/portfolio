"""
Modèle de l'app etudes_de_cas.

Une étude de cas est une analyse structurée : problème → contexte →
analyse → exigences → menaces → architecture → choix → implémentation →
sécurisation → tests → résultats → limites → recommandations.

Workflow de publication identique à Projet et Laboratoire.
"""

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class EtudeDeCasQuerySet(models.QuerySet):
    """QuerySet custom pour filtrer les études de cas publiques."""

    def publies(self):
        now = timezone.now()
        return (
            self.filter(statut=EtudeDeCas.StatutChoices.PUBLIE)
            .filter(models.Q(publish_at__isnull=True) | models.Q(publish_at__lte=now))
            .filter(
                models.Q(unpublish_at__isnull=True)
                | models.Q(unpublish_at__gt=now)
            )
        )


class EtudeDeCas(models.Model):
    """Étude de cas technique (analyse structurée, méthode MERISE-like)."""

    class StatutChoices(models.TextChoices):
        BROUILLON = "brouillon", "Brouillon"
        EN_REVISION = "en_revision", "En révision"
        VALIDE = "valide", "Validé"
        PUBLIE = "publie", "Publié"
        ARCHIVE = "archive", "Archivé"

    # --- Identification ---
    titre = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(
        max_length=200,
        blank=True,
        unique=True,
        verbose_name="Slug",
        help_text="Laisser vide pour génération automatique depuis le titre.",
    )

    # --- Contenu structuré (structure §30) ---
    probleme = models.TextField(blank=True, verbose_name="Problème")
    contexte = models.TextField(blank=True, verbose_name="Contexte")
    analyse = models.TextField(blank=True, verbose_name="Analyse")
    exigences = models.TextField(blank=True, verbose_name="Exigences")
    menaces = models.TextField(blank=True, verbose_name="Menaces")
    architecture_texte = models.TextField(
        blank=True, verbose_name="Architecture (texte)"
    )
    choix_techniques = models.TextField(
        blank=True, verbose_name="Choix techniques"
    )
    implementation = models.TextField(
        blank=True, verbose_name="Implémentation"
    )
    securisation = models.TextField(
        blank=True, verbose_name="Sécurisation"
    )
    tests = models.TextField(blank=True, verbose_name="Tests")
    resultats = models.TextField(blank=True, verbose_name="Résultats")
    limites = models.TextField(blank=True, verbose_name="Limites")
    recommandations = models.TextField(
        blank=True, verbose_name="Recommandations"
    )

    # --- Publication ---
    statut = models.CharField(
        max_length=20,
        choices=StatutChoices.choices,
        default=StatutChoices.BROUILLON,
        verbose_name="Statut",
    )
    publish_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Publication programmée"
    )
    unpublish_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Dépublication programmée"
    )

    # --- Relations ---
    technologies = models.ManyToManyField(
        "technologies.Technologie",
        blank=True,
        related_name="etudes_de_cas",
        verbose_name="Technologies",
    )
    competences = models.ManyToManyField(
        "competences.Competence",
        blank=True,
        related_name="etudes_de_cas",
        verbose_name="Compétences",
    )

    # --- Affichage ---
    ordre = models.PositiveIntegerField(default=0, verbose_name="Ordre")

    # --- SEO ---
    seo_titre = models.CharField(
        max_length=70, blank=True, verbose_name="Titre SEO"
    )
    seo_description = models.CharField(
        max_length=160, blank=True, verbose_name="Description SEO"
    )
    seo_image = models.ForeignKey(
        "medias.Media",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name="Image SEO",
    )

    # --- Auteur et horodatage ---
    auteur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="etudes_de_cas",
        verbose_name="Auteur",
    )
    date_creation = models.DateTimeField(
        auto_now_add=True, verbose_name="Date de création"
    )
    date_modification = models.DateTimeField(
        auto_now=True, verbose_name="Date de modification"
    )

    objects = EtudeDeCasQuerySet.as_manager()

    class Meta:
        verbose_name = "Étude de cas"
        verbose_name_plural = "Études de cas"
        ordering = ["ordre", "-date_creation"]

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

    @property
    def est_public(self) -> bool:
        now = timezone.now()
        if self.statut != self.StatutChoices.PUBLIE:
            return False
        if self.publish_at and self.publish_at > now:
            return False
        if self.unpublish_at and self.unpublish_at <= now:
            return False
        return True