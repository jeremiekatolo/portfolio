"""
Modèle de l'app audits.

Un AuditLog est un enregistrement immuable d'une action sensible.

Règles :
- Aucune modification après création (admin en lecture seule).
- Aucune journalisation de secret (mots de passe, tokens, clés).
- IP stockée en hash SHA-256 (jamais en clair, RGPD).
"""

import hashlib

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class AuditLog(models.Model):
    """Enregistrement immuable d'une action sensible."""

    class ActionChoices(models.TextChoices):
        # --- Authentification ---
        LOGIN_SUCCESS = "login_success", "Connexion réussie"
        LOGIN_FAILED = "login_failed", "Connexion échouée"
        LOGOUT = "logout", "Déconnexion"
        PERMISSION_DENIED = "permission_denied", "Permission refusée"

        # --- Contenus (génériques) ---
        CONTENT_CREATED = "content_created", "Contenu créé"
        CONTENT_UPDATED = "content_updated", "Contenu modifié"
        CONTENT_PUBLISHED = "content_published", "Contenu publié"
        CONTENT_UNPUBLISHED = "content_unpublished", "Contenu dépublié"
        CONTENT_ARCHIVED = "content_archived", "Contenu archivé"
        CONTENT_DELETED = "content_deleted", "Contenu supprimé"

        # --- Médias ---
        MEDIA_UPLOADED = "media_uploaded", "Média uploadé"
        MEDIA_DELETED = "media_deleted", "Média supprimé"

        # --- Autres ---
        USER_CREATED = "user_created", "Utilisateur créé"
        USER_UPDATED = "user_updated", "Utilisateur modifié"
        USER_DELETED = "user_deleted", "Utilisateur supprimé"

        # --- Système ---
        OTHER = "other", "Autre"

    class ResultatChoices(models.TextChoices):
        SUCCES = "succes", "Succès"
        ECHEC = "echec", "Échec"

    # --- Qui ---
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
        verbose_name="Utilisateur",
        help_text="Null pour les actions système ou anonymes.",
    )

    # --- Quoi ---
    action = models.CharField(
        max_length=30,
        choices=ActionChoices.choices,
        verbose_name="Action",
    )

    # --- Sur quoi (liaison polymorphe, optionnelle) ---
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Type de ressource",
    )
    object_id = models.PositiveBigIntegerField(
        null=True, blank=True, verbose_name="ID de la ressource"
    )
    content_object = GenericForeignKey("content_type", "object_id")

    # --- Quand ---
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date")

    # --- Contexte ---
    ip_hash = models.CharField(
        max_length=64,
        blank=True,
        verbose_name="Empreinte IP (SHA-256)",
    )
    resultat = models.CharField(
        max_length=10,
        choices=ResultatChoices.choices,
        default=ResultatChoices.SUCCES,
        verbose_name="Résultat",
    )
    metadonnees = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Métadonnées",
        help_text="Données contextuelles. NE JAMAIS y mettre de secret.",
    )

    class Meta:
        verbose_name = "Entrée d'audit"
        verbose_name_plural = "Journal d'audit"
        ordering = ["-date"]
        indexes = [
            models.Index(fields=["-date"]),
            models.Index(fields=["action"]),
            models.Index(fields=["utilisateur", "-date"]),
            models.Index(fields=["content_type", "object_id"]),
        ]

    def __str__(self) -> str:
        user = self.utilisateur.username if self.utilisateur else "système"
        return f"[{self.date:%Y-%m-%d %H:%M}] {user} — {self.get_action_display()}"

    @staticmethod
    def hasher_ip(ip: str) -> str:
        """Hash SHA-256 d'une IP. Jamais stocker l'IP en clair."""
        if not ip:
            return ""
        return hashlib.sha256(ip.encode("utf-8")).hexdigest()

    def save(self, *args, **kwargs):
        """Empêche toute modification d'un log déjà créé (immuabilité)."""
        if self.pk is not None:
            raise ValueError(
                "Un AuditLog est immuable : il ne peut pas être modifié après création."
            )
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Empêche la suppression manuelle (politique de rétention à définir)."""
        raise ValueError(
            "Un AuditLog ne peut pas être supprimé manuellement. "
            "Utiliser une commande de purge avec politique de rétention."
        )