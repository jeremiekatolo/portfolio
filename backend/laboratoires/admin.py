"""
Admin Django complet pour l'app laboratoires.
"""

from django.contrib import admin

from medias.admin import LienExterneInline, MediaLienInline

from .models import Laboratoire


@admin.register(Laboratoire)
class LaboratoireAdmin(admin.ModelAdmin):
    list_display = (
        "titre",
        "difficulte",
        "statut",
        "ordre",
        "auteur",
        "date_creation",
    )
    list_filter = ("statut", "difficulte", "technologies", "competences")
    search_fields = ("titre", "slug", "objectif", "problematique")
    prepopulated_fields = {"slug": ("titre",)}
    autocomplete_fields = ("seo_image", "auteur")
    filter_horizontal = ("technologies", "competences")
    readonly_fields = ("date_creation", "date_modification")
    date_hierarchy = "date_creation"
    inlines = [MediaLienInline, LienExterneInline]

    fieldsets = (
        ("Identification", {"fields": ("titre", "slug")}),
        (
            "Objectif et problématique",
            {"fields": ("objectif", "problematique", "prerequis")},
        ),
        (
            "Environnement",
            {
                "fields": (
                    "environnement",
                    "materiel_vm",
                    "architecture_texte",
                )
            },
        ),
        (
            "Configuration et tests",
            {"fields": ("configuration", "tests")},
        ),
        (
            "Résultats et analyse",
            {
                "fields": (
                    "resultats",
                    "incidents_rencontres",
                    "corrections",
                    "analyse_securite",
                    "limites",
                    "ameliorations",
                )
            },
        ),
        (
            "Publication",
            {
                "fields": (
                    "statut",
                    "publish_at",
                    "unpublish_at",
                    "difficulte",
                    "ordre",
                )
            },
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