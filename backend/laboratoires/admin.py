"""
Admin Django minimal pour l'app laboratoires.

Version minimale pour supporter l'autocomplete dans ProjetAdmin.
Sera completé à l'Étape G.
"""

from django.contrib import admin

from .models import Laboratoire


@admin.register(Laboratoire)
class LaboratoireAdmin(admin.ModelAdmin):
    list_display = ("titre", "slug")
    search_fields = ("titre", "slug")
    prepopulated_fields = {"slug": ("titre",)}
    ordering = ("titre",)