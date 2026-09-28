"""
Modèles de l'app competences.

Un seul modèle : Competence.

Une compétence est une capacité, identifiée par un domaine
(réseaux, cybersécurité, systèmes, automatisation, développement).

Règles :
- Aucun champ `pourcentage` ou `niveau`.
- La preuve remplace la notation (projets, labs, études de cas).
- `nom` unique.
"""

from django.db import models


class Competence(models.Model):
    """Compétence métier, sans évaluation chiffrée."""

    class DomaineChoices(models.TextChoices):
        RESEAUX = "reseaux", "Réseaux"
        CYBERSECURITE = "cybersecurite", "Cybersécurité"
        SYSTEMES = "systemes", "Systèmes"
        AUTOMATISATION = "automatisation", "Automatisation"
        DEVELOPPEMENT = "developpement", "Développement d'ingénierie"

    nom = models.CharField(
        max_length=150, unique=True, verbose_name="Nom"
    )
    domaine = models.CharField(
        max_length=30,
        choices=DomaineChoices.choices,
        verbose_name="Domaine",
    )
    description = models.TextField(
        blank=True, verbose_name="Description"
    )
    ordre = models.PositiveIntegerField(default=0, verbose_name="Ordre")

    class Meta:
        verbose_name = "Compétence"
        verbose_name_plural = "Compétences"
        ordering = ["domaine", "ordre", "nom"]

    def __str__(self) -> str:
        return f"[{self.get_domaine_display()}] {self.nom}"