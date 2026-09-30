"""
Modèle de l'app projets.

Un projet est un contenu central du portfolio. Il possède :
- Un cycle de publication (brouillon → publié).
- Des relations N..N avec technologies et competences.
- Des FK optionnelles vers laboratoire et etude_de_cas.
- Des médias et liens externes (via les apps medias).

Règles de slug (validées Phase 2) :
- Pré-rempli dans l'admin depuis `titre`.
- Modifiable manuellement.
- Fallback serveur si vide.
- Unique.
- 200 caractères max.
- Changement interdit après publication (contrôlé en Phase 6).
"""

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class ProjetQuerySet(models.QuerySet):
    """QuerySet custom pour filtrer les projets publics."""

    def publies(self):
        """Retourne uniquement les projets visibles publiquement."""
        now = timezone.now()
        return (
            self.filter(statut=Projet.StatutChoices.PUBLIE)
            .filter(models.Q(publish_at__isnull=True) | models.Q(publish_at__lte=now))
            .filter(
                models.Q(unpublish_at__isnull=True)
                | models.Q(unpublish_at__gt=now)
            )
        )


class Projet(models.Model):
    """Projet technique présenté dans le portfolio."""

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

    # --- Contenu ---
    resume = models.CharField(max_length=500, blank=True, verbose_name="Résumé")
    description = models.TextField(blank=True, verbose_name="Description")
    probleme = models.TextField(blank=True, verbose_name="Problème")
    contexte = models.TextField(blank=True, verbose_name="Contexte")
    objectifs = models.TextField(blank=True, verbose_name="Objectifs")
    architecture_texte = models.TextField(
        blank=True, verbose_name="Architecture (texte)"
    )
    role = models.CharField(max_length=200, blank=True, verbose_name="Rôle")
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

    # --- Métadonnées ---
    date_realisation = models.DateField(
        null=True, blank=True, verbose_name="Date de réalisation"
    )
    duree = models.CharField(max_length=100, blank=True, verbose_name="Durée")
    resultats = models.TextField(blank=True, verbose_name="Résultats")
    limites = models.TextField(blank=True, verbose_name="Limites")
    ameliorations_futures = models.TextField(
        blank=True, verbose_name="Améliorations futures"
    )

    # --- Relations ---
    categorie = models.ForeignKey(
        "categories.Categorie",
        on_delete=models.PROTECT,
        related_name="projets",
        verbose_name="Catégorie",
    )
    laboratoire = models.ForeignKey(
        "laboratoires.Laboratoire",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="projets",
        verbose_name="Laboratoire lié",
    )
    etude_de_cas = models.ForeignKey(
        "etudes_de_cas.EtudeDeCas",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="projets",
        verbose_name="Étude de cas liée",
    )
    technologies = models.ManyToManyField(
        "technologies.Technologie",
        blank=True,
        related_name="projets",
        verbose_name="Technologies",
    )
    competences = models.ManyToManyField(
        "competences.Competence",
        blank=True,
        related_name="projets",
        verbose_name="Compétences",
    )

    # --- Affichage ---
    mis_en_avant = models.BooleanField(
        default=False, verbose_name="Mis en avant"
    )
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
        related_name="projets",
        verbose_name="Auteur",
    )
    date_creation = models.DateTimeField(
        auto_now_add=True, verbose_name="Date de création"
    )
    date_modification = models.DateTimeField(
        auto_now=True, verbose_name="Date de modification"
    )

    # --- Manager ---
    objects = ProjetQuerySet.as_manager()

    class Meta:
        verbose_name = "Projet"
        verbose_name_plural = "Projets"
        ordering = ["-mis_en_avant", "ordre", "-date_realisation"]

    def __str__(self) -> str:
        return self.titre

    def save(self, *args, **kwargs):
        """Génère un slug unique si vide."""
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
        """Un projet est public si son statut et ses dates le permettent."""
        now = timezone.now()
        if self.statut != self.StatutChoices.PUBLIE:
            return False
        if self.publish_at and self.publish_at > now:
            return False
        if self.unpublish_at and self.unpublish_at <= now:
            return False
        return True