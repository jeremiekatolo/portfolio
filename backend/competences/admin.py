"""
Admin Django pour l'app competences.

- Pas de slug.
- Pas de pourcentage ni de niveau (règle métier stricte).
- Filtres par domaine.
"""

from django.contrib import admin

from .models import Competence


@admin.register(Competence)
class CompetenceAdmin(admin.ModelAdmin):
    list_display = ("nom", "domaine", "ordre")
    list_filter = ("domaine",)
    search_fields = ("nom", "description")
    ordering = ("domaine", "ordre", "nom")
    list_editable = ("ordre",)
    list_per_page = 50

    fieldsets = (
        (None, {"fields": ("nom", "domaine")}),
        ("Détails", {"fields": ("description", "ordre")}),
    )