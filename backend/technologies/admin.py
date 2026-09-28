"""
Admin Django pour l'app technologies.

- Pas de slug (non exposé en URL).
- Logo optionnel (FK Media), avec autocomplete.
- Filtres par catégorie technique.
"""

from django.contrib import admin

from .models import Technologie


@admin.register(Technologie)
class TechnologieAdmin(admin.ModelAdmin):
    list_display = (
        "nom",
        "categorie_tech",
        "url_officielle",
        "ordre",
    )
    list_filter = ("categorie_tech",)
    search_fields = ("nom", "description")
    autocomplete_fields = ("logo",)
    ordering = ("categorie_tech", "ordre", "nom")
    list_editable = ("ordre",)
    list_per_page = 30

    fieldsets = (
        (None, {"fields": ("nom", "categorie_tech", "logo")}),
        ("Détails", {"fields": ("description", "url_officielle", "ordre")}),
    )