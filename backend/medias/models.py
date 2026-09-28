"""
Modèles de l'app medias.

Trois modèles :
- Media       : fichier uploadé (image, schéma, PDF, vidéo, ...)
- MediaLien   : liaison polymorphe entre un Media et un contenu
- LienExterne : liaison polymorphe entre un contenu et une URL externe
                (GitHub, démo, documentation, vidéo, ...)

Règles :
- Aucun contenu réel dans ce fichier.
- Le champ `est_orphelin` est maintenu par une commande de nettoyage (Phase 6+).
- Les validations de taille / MIME / extension seront ajoutées en Phase 6.
"""

from __future__ import annotations

import hashlib
from datetime import date
from pathlib import Path

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.text import slugify


# ---------------------------------------------------------------------------
# Utilitaires
# ---------------------------------------------------------------------------


def media_upload_path(instance: "Media", filename: str) -> str:
    """
    Organise les fichiers uploadés par type et date.

    Exemple : medias/image/2026/09/mon-schema.png
    """
    ext = Path(filename).suffix.lower()
    stem = Path(filename).stem
    slug = slugify(stem)[:80] or "media"
    today = date.today()
    type_folder = instance.type or Media.TypeChoices.AUTRE
    return f"medias/{type_folder}/{today.year}/{today.month:02d}/{slug}{ext}"


# ---------------------------------------------------------------------------
# Media
# ---------------------------------------------------------------------------


class Media(models.Model):
    """Fichier uploadé et réutilisable."""

    class TypeChoices(models.TextChoices):
        IMAGE = "image", "Image"
        SCHEMA = "schema", "Schéma"
        PDF = "pdf", "PDF"
        VIDEO = "video", "Vidéo"
        AUTRE = "autre", "Autre"

    fichier = models.FileField(
        upload_to=media_upload_path,
        verbose_name="Fichier",
    )
    nom_original = models.CharField(
        max_length=255, blank=True, verbose_name="Nom d'origine"
    )
    mime_type = models.CharField(
        max_length=100, blank=True, verbose_name="Type MIME"
    )
    taille = models.PositiveBigIntegerField(
        default=0, verbose_name="Taille (octets)"
    )
    hash_sha256 = models.CharField(
        max_length=64,
        unique=True,
        blank=True,
        null=True,
        verbose_name="Empreinte SHA-256",
        help_text="Sert à détecter les doublons.",
    )
    type = models.CharField(
        max_length=20,
        choices=TypeChoices.choices,
        default=TypeChoices.AUTRE,
        verbose_name="Type",
    )
    alt_text = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Texte alternatif",
        help_text="Pour l'accessibilité (lecteurs d'écran, SEO).",
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="medias_uploades",
        verbose_name="Uploadé par",
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Uploadé le"
    )
    est_orphelin = models.BooleanField(
        default=False,
        verbose_name="Orphelin",
        help_text="Aucun contenu ne référence ce média (mis à jour par une commande).",
    )

    class Meta:
        verbose_name = "Média"
        verbose_name_plural = "Médias"
        ordering = ["-uploaded_at"]

    def __str__(self) -> str:
        return self.nom_original or Path(self.fichier.name).name or f"Media #{self.pk}"

    def save(self, *args, **kwargs):
        """
        Calcule automatiquement :
        - nom_original
        - mime_type
        - taille
        - hash_sha256 (si le fichier est nouveau)
        """
        if self.fichier and not self.hash_sha256:
            self.nom_original = self.nom_original or Path(self.fichier.name).name
            self.taille = self.taille or self.fichier.size
            self.mime_type = (
                self.mime_type
                or getattr(self.fichier.file, "content_type", "")
                or ""
            )
            h = hashlib.sha256()
            for chunk in self.fichier.chunks():
                h.update(chunk)
            self.hash_sha256 = h.hexdigest()
            self.fichier.seek(0)
        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------
# MediaLien (polymorphe)
# ---------------------------------------------------------------------------


class MediaLien(models.Model):
    """Liaison polymorphe entre un Media et n'importe quel contenu."""

    class RoleChoices(models.TextChoices):
        COUVERTURE = "couverture", "Couverture"
        ILLUSTRATION = "illustration", "Illustration"
        SCHEMA = "schema", "Schéma"
        CAPTURE = "capture", "Capture d'écran"
        AUTRE = "autre", "Autre"

    media = models.ForeignKey(
        Media,
        on_delete=models.CASCADE,
        related_name="liens",
        verbose_name="Média",
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name="Type de contenu",
    )
    object_id = models.PositiveBigIntegerField(verbose_name="ID de l'objet")
    content_object = GenericForeignKey("content_type", "object_id")

    role = models.CharField(
        max_length=20,
        choices=RoleChoices.choices,
        default=RoleChoices.ILLUSTRATION,
        verbose_name="Rôle",
    )
    ordre = models.PositiveIntegerField(default=0, verbose_name="Ordre")
    légende = models.CharField(
        max_length=255, blank=True, verbose_name="Légende"
    )

    class Meta:
        verbose_name = "Lien média"
        verbose_name_plural = "Liens médias"
        ordering = ["ordre", "id"]
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    def __str__(self) -> str:
        return f"{self.media} → {self.content_type}#{self.object_id}"


# ---------------------------------------------------------------------------
# LienExterne (polymorphe)
# ---------------------------------------------------------------------------


class LienExterne(models.Model):
    """Liaison polymorphe entre un contenu et une URL externe."""

    class TypeChoices(models.TextChoices):
        GITHUB = "github", "GitHub"
        DEMO = "demo", "Démonstration"
        DOCUMENTATION = "documentation", "Documentation"
        VIDEO = "video", "Vidéo"
        ARTICLE = "article", "Article externe"
        AUTRE = "autre", "Autre"

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name="Type de contenu",
    )
    object_id = models.PositiveBigIntegerField(verbose_name="ID de l'objet")
    content_object = GenericForeignKey("content_type", "object_id")

    type = models.CharField(
        max_length=20,
        choices=TypeChoices.choices,
        default=TypeChoices.AUTRE,
        verbose_name="Type",
    )
    url = models.URLField(max_length=500, verbose_name="URL")
    label = models.CharField(
        max_length=100, blank=True, verbose_name="Libellé"
    )
    ordre = models.PositiveIntegerField(default=0, verbose_name="Ordre")

    class Meta:
        verbose_name = "Lien externe"
        verbose_name_plural = "Liens externes"
        ordering = ["ordre", "id"]
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    def __str__(self) -> str:
        return f"{self.get_type_display()} — {self.url}"