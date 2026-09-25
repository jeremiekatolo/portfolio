"""
Modèles de l'app utilisateurs.

Deux modèles :
- Utilisateur : modèle custom, hérite de AbstractUser, ajoute le champ `role`.
- Profil      : informations publiques, 1-1 avec Utilisateur.

Règles :
- Aucun pourcentage, aucune donnée inventée.
- Les champs photo/cv/seo_image seront ajoutés à l'étape 2.2 (media).
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class Utilisateur(AbstractUser):
    """
    Utilisateur custom du portfolio.

    Hérite de AbstractUser (username, email, password, is_staff,
    is_active, is_superuser, date_joined, last_login, ...).
    Ajoute un champ `role` pour le contrôle d'accès applicatif.
    """

    class Role(models.TextChoices):
        VISITEUR = "visiteur", "Visiteur"
        EDITEUR = "editeur", "Éditeur"
        ADMINISTRATEUR = "administrateur", "Administrateur"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.VISITEUR,
        verbose_name="Rôle",
        help_text="Rôle applicatif (indépendant de is_superuser/is_staff).",
    )

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ["username"]

    def __str__(self) -> str:
        return self.username


class Profil(models.Model):
    """
    Profil public du propriétaire du portfolio.

    Relation 1-1 avec Utilisateur.
    Le profil porte les informations de présentation et les valeurs
    SEO par défaut utilisées quand un contenu n'a pas d'override.
    """

    utilisateur = models.OneToOneField(
        "utilisateurs.Utilisateur",
        on_delete=models.CASCADE,
        related_name="profil",
        verbose_name="Utilisateur",
    )

    # --- Identité publique ---
    nom_public = models.CharField(
        max_length=100, blank=True, verbose_name="Nom public"
    )
    titre_principal = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Titre principal",
        help_text='Ex. : "Network & Cybersecurity Engineer".',
    )
    titre_secondaire = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Titre secondaire",
        help_text='Ex. : "Ingénieur Réseaux & Cybersécurité".',
    )
    bio_courte = models.CharField(
        max_length=300, blank=True, verbose_name="Bio courte"
    )
    bio_longue = models.TextField(blank=True, verbose_name="Bio longue")

    # --- Contact public ---
    email_public = models.EmailField(blank=True, verbose_name="Email public")
    telephone_public = models.CharField(
        max_length=30, blank=True, verbose_name="Téléphone public"
    )
    localisation = models.CharField(
        max_length=100, blank=True, verbose_name="Localisation"
    )

    # --- Disponibilité ---
    disponible = models.BooleanField(
        default=False, verbose_name="Disponible pour missions"
    )

    # --- SEO par défaut ---
    seo_titre_defaut = models.CharField(
        max_length=70, blank=True, verbose_name="Titre SEO par défaut"
    )
    seo_description_defaut = models.CharField(
        max_length=160, blank=True, verbose_name="Description SEO par défaut"
    )

    # --- Horodatage ---
    date_creation = models.DateTimeField(
        auto_now_add=True, verbose_name="Date de création"
    )
    date_modification = models.DateTimeField(
        auto_now=True, verbose_name="Date de modification"
    )

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profils"

    def __str__(self) -> str:
        return f"Profil de {self.utilisateur.username}"