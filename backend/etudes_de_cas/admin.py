"""
Admin Django minimal pour l'app etudes_de_cas.

Version minimale pour supporter l'autocomplete dans ProjetAdmin.
Sera completé à l'Étape H.
"""

from django.contrib import admin

from .models import EtudeDeCas


@admin.register(EtudeDeCas)
class EtudeDeCasAdmin(admin.ModelAdmin):
    list_display = ("titre", "slug")
    search_fields = ("titre", "slug")
    prepopulated_fields = {"slug": ("titre",)}
    ordering = ("titre",)