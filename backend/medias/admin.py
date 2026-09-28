"""
Configuration de l'admin Django pour l'app medias.

- Media       : liste avec type, taille lisible, hash, orphelin.
- MediaLien   : liaison polymorphe.
- LienExterne : liaison polymorphe.

MediaLienInline et LienExterneInline sont réutilisables dans
les admin des apps contenus (projets, labos, articles, etc.).
"""

from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import LienExterne, Media, MediaLien


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nom_original",
        "type",
        "taille_affichee",
        "uploaded_by",
        "uploaded_at",
        "est_orphelin",
    )
    list_filter = ("type", "est_orphelin", "uploaded_at")
    search_fields = ("nom_original", "alt_text", "hash_sha256")
    readonly_fields = (
        "nom_original",
        "mime_type",
        "taille",
        "hash_sha256",
        "uploaded_at",
        "est_orphelin",
    )
    date_hierarchy = "uploaded_at"
    ordering = ("-uploaded_at",)

    fieldsets = (
        ("Fichier", {"fields": ("fichier", "type", "alt_text")}),
        (
            "Métadonnées",
            {
                "fields": (
                    "nom_original",
                    "mime_type",
                    "taille",
                    "hash_sha256",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Suivi",
            {
                "fields": ("uploaded_by", "uploaded_at", "est_orphelin"),
                "classes": ("collapse",),
            },
        ),
    )

    @admin.display(description="Taille")
    def taille_affichee(self, obj: Media) -> str:
        """Affiche la taille en Ko/Mo de façon lisible."""
        if not obj.taille:
            return "—"
        ko = obj.taille / 1024
        if ko < 1024:
            return f"{ko:.1f} Ko"
        return f"{ko / 1024:.2f} Mo"


class MediaLienInline(GenericTabularInline):
    """Inline générique pour les médias liés à un contenu."""

    model = MediaLien
    extra = 0
    fields = ("media", "role", "ordre", "légende")
    autocomplete_fields = ("media",)
    ordering = ("ordre", "id")
    verbose_name = "Lien média"
    verbose_name_plural = "Liens médias"


class LienExterneInline(GenericTabularInline):
    """Inline générique pour les liens externes liés à un contenu."""

    model = LienExterne
    extra = 0
    fields = ("type", "url", "label", "ordre")
    ordering = ("ordre", "id")
    verbose_name = "Lien externe"
    verbose_name_plural = "Liens externes"


@admin.register(MediaLien)
class MediaLienAdmin(admin.ModelAdmin):
    list_display = ("id", "media", "content_type", "object_id", "role", "ordre")
    list_filter = ("role", "content_type")
    search_fields = ("media__nom_original", "légende")
    autocomplete_fields = ("media",)
    ordering = ("content_type", "object_id", "ordre")


@admin.register(LienExterne)
class LienExterneAdmin(admin.ModelAdmin):
    list_display = ("id", "type", "url", "label", "content_type", "object_id")
    list_filter = ("type", "content_type")
    search_fields = ("url", "label")
    ordering = ("content_type", "object_id", "ordre")