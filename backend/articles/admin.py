"""
Admin Django pour l'app articles.
"""

from django.contrib import admin

from medias.admin import LienExterneInline, MediaLienInline

from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "titre",
        "categorie",
        "statut",
        "temps_lecture",
        "ordre",
        "auteur",
        "date_creation",
    )
    list_filter = ("statut", "categorie", "technologies", "competences")
    search_fields = ("titre", "slug", "resume", "contenu")
    prepopulated_fields = {"slug": ("titre",)}
    autocomplete_fields = ("categorie", "seo_image", "auteur")
    filter_horizontal = ("technologies", "competences")
    readonly_fields = ("date_creation", "date_modification", "temps_lecture")
    date_hierarchy = "date_creation"
    inlines = [MediaLienInline, LienExterneInline]

    fieldsets = (
        ("Identification", {"fields": ("titre", "slug", "resume")}),
        ("Contenu", {"fields": ("contenu", "temps_lecture")}),
        (
            "Publication",
            {"fields": ("statut", "publish_at", "unpublish_at", "ordre")},
        ),
        ("Catégorie et relations", {"fields": ("categorie", "technologies", "competences")}),
        ("SEO", {"fields": ("seo_titre", "seo_description", "seo_image")}),
        (
            "Auteur et horodatage",
            {
                "fields": ("auteur", "date_creation", "date_modification"),
                "classes": ("collapse",),
            },
        ),
    )