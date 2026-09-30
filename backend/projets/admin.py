"""
Admin Django pour l'app projets.

- Inlines : MediaLienInline + LienExterneInline (réutilisables).
- Prepopulated slug depuis `titre`.
- Autocomplete sur les FK et M2M.
- Filtres : statut, difficulté, catégorie, mis_en_avant.
"""

from django.contrib import admin

from medias.admin import LienExterneInline, MediaLienInline

from .models import Projet


@admin.register(Projet)
class ProjetAdmin(admin.ModelAdmin):
    list_display = (
        "titre",
        "categorie",
        "difficulte",
        "statut",
        "mis_en_avant",
        "date_realisation",
        "auteur",
    )
    list_filter = (
        "statut",
        "difficulte",
        "categorie",
        "mis_en_avant",
        "technologies",
        "competences",
    )
    search_fields = ("titre", "slug", "resume", "description")
    prepopulated_fields = {"slug": ("titre",)}
    autocomplete_fields = (
        "categorie",
        "laboratoire",
        "etude_de_cas",
        "seo_image",
        "auteur",
    )
    filter_horizontal = ("technologies", "competences")
    readonly_fields = ("date_creation", "date_modification")
    date_hierarchy = "date_creation"
    inlines = [MediaLienInline, LienExterneInline]

    fieldsets = (
        ("Identification", {"fields": ("titre", "slug", "resume")}),
        (
            "Contenu",
            {
                "fields": (
                    "description",
                    "probleme",
                    "contexte",
                    "objectifs",
                    "architecture_texte",
                    "role",
                    "difficulte",
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
                    "mis_en_avant",
                    "ordre",
                )
            },
        ),
        (
            "Métadonnées",
            {
                "fields": (
                    "date_realisation",
                    "duree",
                    "resultats",
                    "limites",
                    "ameliorations_futures",
                )
            },
        ),
        (
            "Relations",
            {
                "fields": (
                    "categorie",
                    "laboratoire",
                    "etude_de_cas",
                    "technologies",
                    "competences",
                )
            },
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