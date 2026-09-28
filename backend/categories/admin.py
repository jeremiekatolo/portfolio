"""
Admin Django pour l'app categories.

- Prepopulated slug depuis `nom`.
- Filtres par type, recherche par nom et slug.
- Slug protégé après publication : géré par le modèle Contenu (Phase 2.6+).
  Ici, la catégorie n'a pas d'état publié/dépublié, donc le slug reste
  modifiable tant qu'aucun contenu publié ne l'utilise.
"""

from django.contrib import admin

from .models import Categorie


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ("nom", "type", "slug", "ordre")
    list_filter = ("type",)
    search_fields = ("nom", "slug", "description")
    prepopulated_fields = {"slug": ("nom",)}
    ordering = ("type", "ordre", "nom")
    list_editable = ("ordre",)
    list_per_page = 30

    fieldsets = (
        (None, {"fields": ("nom", "slug", "type")}),
        ("Détails", {"fields": ("description", "ordre")}),
    )