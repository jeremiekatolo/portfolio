"""
Admin Django complet pour l'app etudes_de_cas.
"""

from django.contrib import admin

from medias.admin import LienExterneInline, MediaLienInline

from .models import EtudeDeCas


@admin.register(EtudeDeCas)
class EtudeDeCasAdmin(admin.ModelAdmin):
    list_display = (
        "titre",
        "statut",
        "ordre",
        "auteur",
        "date_creation",
    )
    list_filter = ("statut", "technologies", "competences")
    search_fields = ("titre", "slug", "probleme", "contexte", "analyse")
    prepopulated_fields = {"slug": ("titre",)}
    autocomplete_fields = ("seo_image", "auteur")
    filter_horizontal = ("technologies", "competences")
    readonly_fields = ("date_creation", "date_modification")
    date_hierarchy = "date_creation"
    inlines = [MediaLienInline, LienExterneInline]

    fieldsets = (
        ("Identification", {"fields": ("titre", "slug")}),
        (
            "Analyse",
            {
                "fields": (
                    "probleme",
                    "contexte",
                    "analyse",
                    "exigences",
                    "menaces",
                )
            },
        ),
        (
            "Solution",
            {
                "fields": (
                    "architecture_texte",
                    "choix_techniques",
                    "implementation",
                    "securisation",
                )
            },
        ),
        (
            "Résultats",
            {
                "fields": (
                    "tests",
                    "resultats",
                    "limites",
                    "recommandations",
                )
            },
        ),
        (
            "Publication",
            {"fields": ("statut", "publish_at", "unpublish_at", "ordre")},
        ),
        (
            "Relations",
            {"fields": ("technologies", "competences")},
        ),
        (
            "SEO",
            {"fields": ("seo_titre", "seo_description", "seo_image")},
        ),
        (
            "Auteur et horodatage",
            {
                "fields": ("auteur", "date_creation", "date_modification"),
                "classes": ("collapse",),
            },
        ),
    )