"""
Modèle de l'app laboratoires.

Un laboratoire est une expérimentation technique documentée :
objectif, environnement, configuration, tests, résultats, limites.

Workflow de publication identique à Projet.
"""

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class LaboratoireQuerySet(models.QuerySet):
    """QuerySet custom pour filtrer les labos publics."""

    def publies(self):
        now = timezone.now()
        return (
            self.filter(statut=Laboratoire.StatutChoices.PUBLIE)
            .filter(models.Q(publish_at__isnull=True) | models.Q(publish_at__lte=now))
            .filter(
                models.Q(unpublish_at__isnull=True)
                | models.Q(unpublish_at__gt=now)
            )
        )


class Laboratoire(models.Model):
    """Laboratoire technique (expérimentation, lab, POC)."""

    class StatutChoices(models.TextChoices):
        BROUILLON = "brouillon", "Brouillon"
        EN_REVISION = "en_revision", "En révision"
        VALIDE = "valide", "Validé"
        PUBLIE = "publie", "Publié"
        ARCHIVE = "archive", "Archivé"

    class DifficulteChoices(models.TextChoices):
        DEBUTANT = "debutant", "Débutant"
        INTERMEDIAIRE = "intermediaire", "Intermédiaire"
        AVANCE = "avance", "Avancé"
        EXPERT = "expert", "Expert"

    # --- Identification ---
    titre = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(
        max_length=200,
        blank=True,
        unique=True,
        verbose_name="Slug",
        help_text="Laisser vide pour génération automatique depuis le titre.",
    )

    # --- Contenu technique (structure §29) ---
    objectif = models.TextField(blank=True, verbose_name="Objectif")
    problematique = models.TextField(blank=True, verbose_name="Problématique")
    environnement = models.TextField(
        blank=True, verbose_name="Environnement"
    )
    architecture_texte = models.TextField(
        blank=True, verbose_name="Architecture (texte)"
    )
    materiel_vm = models.TextField(
        blank=True, verbose_name="Matériel / VM utilisés"
    )
    prerequis = models.TextField(blank=True, verbose_name="Pré-requis")
    configuration = models.TextField(
        blank=True, verbose_name="Configuration"
    )
    tests = models.TextField(blank=True, verbose_name="Tests réalisés")
    resultats = models.TextField(blank=True, verbose_name="Résultats")
    incidents_rencontres = models.TextField(
        blank=True, verbose_name="Incidents rencontrés"
    )
    corrections = models.TextField(
        blank=True, verbose_name="Corrections apportées"
    )
    analyse_securite = models.TextField(
        blank=True, verbose_name="Analyse sécurité"
    )
    limites = models.TextField(blank=True, verbose_name="Limites")
    ameliorations = models.TextField(
        blank=True, verbose_name="Améliorations futures"
    )

    # --- Métadonnées ---
    difficulte = models.CharField(
        max_length=20,
        choices=DifficulteChoices.choices,
        default=DifficulteChoices.INTERMEDIAIRE,
        verbose_name="Difficulté",
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
        related_name="laboratoires",
        verbose_name="Technologies",
    )
    competences = models.ManyToManyField(
        "competences.Competence",
        blank=True,
        related_name="laboratoires",
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
        related_name="laboratoires",
        verbose_name="Auteur",
    )
    date_creation = models.DateTimeField(
        auto_now_add=True, verbose_name="Date de création"
    )
    date_modification = models.DateTimeField(
        auto_now=True, verbose_name="Date de modification"
    )

    objects = LaboratoireQuerySet.as_manager()

    class Meta:
        verbose_name = "Laboratoire"
        verbose_name_plural = "Laboratoires"
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