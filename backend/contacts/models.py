"""
Modèle de l'app contacts.

Un Contact représente un message envoyé via le formulaire public.
- Anti-spam basique (honeypot côté serializer, validation, rate limiting Phase 6).
- IP stockée en hash SHA-256 (jamais en clair, RGPD).
- Statut : nouveau / lu / traité / spam.
"""

import hashlib

from django.db import models


class Contact(models.Model):
    """Message envoyé via le formulaire de contact."""

    class StatutChoices(models.TextChoices):
        NOUVEAU = "nouveau", "Nouveau"
        LU = "lu", "Lu"
        TRAITE = "traite", "Traité"
        SPAM = "spam", "Spam"

    nom = models.CharField(max_length=150, verbose_name="Nom")
    email = models.EmailField(verbose_name="Email")
    sujet = models.CharField(max_length=200, verbose_name="Sujet")
    message = models.TextField(verbose_name="Message")

    date_envoi = models.DateTimeField(
        auto_now_add=True, verbose_name="Date d'envoi"
    )
    ip_hash = models.CharField(
        max_length=64,
        blank=True,
        verbose_name="Empreinte IP (SHA-256)",
        help_text="Jamais l'IP en clair (RGPD).",
    )
    user_agent = models.CharField(
        max_length=300, blank=True, verbose_name="User-Agent"
    )

    statut = models.CharField(
        max_length=20,
        choices=StatutChoices.choices,
        default=StatutChoices.NOUVEAU,
        verbose_name="Statut",
    )

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
        ordering = ["-date_envoi"]

    def __str__(self) -> str:
        return f"{self.nom} — {self.sujet}"

    @staticmethod
    def hasher_ip(ip: str) -> str:
        """Hash SHA-256 d'une adresse IP. Jamais stocker l'IP en clair."""
        if not ip:
            return ""
        return hashlib.sha256(ip.encode("utf-8")).hexdigest()