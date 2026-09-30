"""
Modèles de l'app parcours.

Deux modèles :
- Parcours      : une entrée du parcours professionnel (expérience, formation).
- Certification : une certification obtenue.

Tous deux sont rattachés au Profil (propriétaire unique du portfolio).
Ils peuvent référencer plusieurs Compétences (M2M).
Pas de slug : non exposés en URL individuelle.
"""

from django.db import models


class Parcours(models.Model):
    """Entrée du parcours professionnel : expérience ou formation."""

    class TypeChoices(models.TextChoices):
        EXPERIENCE = "experience", "Expérience professionnelle"
        FORMATION = "formation", "Formation"

    profil = models.ForeignKey(
        "utilisateurs.Profil",
        on_delete=models.CASCADE,
        related_name="parcours",
        verbose_name="Profil",
    )
    titre = models.CharField(max_length=200, verbose_name="Titre")
    type = models.CharField(
        max_length=20,
        choices=TypeChoices.choices,
        verbose_name="Type",
    )
    organisation = models.CharField(
        max_length=200, blank=True, verbose_name="Organisation"
    )
    lieu = models.CharField(max_length=150, blank=True, verbose_name="Lieu")
    date_debut = models.DateField(verbose_name="Date de début")
    date_fin = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date de fin",
        help_text="Laisser vide si en cours.",
    )
    description = models.TextField(blank=True, verbose_name="Description")
    ordre = models.PositiveIntegerField(default=0, verbose_name="Ordre")
    competences = models.ManyToManyField(
        "competences.Competence",
        blank=True,
        related_name="parcours",
        verbose_name="Compétences",
    )

    class Meta:
        verbose_name = "Parcours"
        verbose_name_plural = "Parcours"
        ordering = ["-date_debut", "ordre"]

    def __str__(self) -> str:
        return f"{self.titre} ({self.get_type_display()})"

    @property
    def est_en_cours(self) -> bool:
        return self.date_fin is None


class Certification(models.Model):
    """Certification obtenue (ou en cours si date_expiration nulle)."""

    profil = models.ForeignKey(
        "utilisateurs.Profil",
        on_delete=models.CASCADE,
        related_name="certifications",
        verbose_name="Profil",
    )
    nom = models.CharField(max_length=200, verbose_name="Nom")
    organisme = models.CharField(
        max_length=200, blank=True, verbose_name="Organisme"
    )
    date_obtention = models.DateField(verbose_name="Date d'obtention")
    date_expiration = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date d'expiration",
        help_text="Laisser vide si la certification n'expire pas.",
    )
    identifiant = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Identifiant",
        help_text="Numéro ou identifiant de la certification.",
    )
    url_verification = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="URL de vérification",
    )
    description = models.TextField(blank=True, verbose_name="Description")
    badge = models.ForeignKey(
        "medias.Media",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name="Badge",
    )
    ordre = models.PositiveIntegerField(default=0, verbose_name="Ordre")
    competences = models.ManyToManyField(
        "competences.Competence",
        blank=True,
        related_name="certifications",
        verbose_name="Compétences",
    )

    class Meta:
        verbose_name = "Certification"
        verbose_name_plural = "Certifications"
        ordering = ["-date_obtention", "ordre"]

    def __str__(self) -> str:
        return self.nom

    @property
    def est_expiree(self) -> bool:
        """Vrai si la certification a une date d'expiration passée."""
        from django.utils import timezone

        if not self.date_expiration:
            return False
        return self.date_expiration < timezone.now().date()