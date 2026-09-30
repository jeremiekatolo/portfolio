"""
Admin Django pour l'app parcours.
"""

from django.contrib import admin

from .models import Certification, Parcours


@admin.register(Parcours)
class ParcoursAdmin(admin.ModelAdmin):
    list_display = (
        "titre",
        "type",
        "organisation",
        "date_debut",
        "date_fin",
        "ordre",
    )
    list_filter = ("type",)
    search_fields = ("titre", "organisation", "description")
    autocomplete_fields = ("profil",)
    filter_horizontal = ("competences",)
    list_editable = ("ordre",)
    ordering = ("-date_debut", "ordre")
    date_hierarchy = "date_debut"

    fieldsets = (
        ("Identification", {"fields": ("profil", "titre", "type", "ordre")}),
        (
            "Détails",
            {"fields": ("organisation", "lieu", "date_debut", "date_fin", "description")},
        ),
        ("Compétences", {"fields": ("competences",)}),
    )


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = (
        "nom",
        "organisme",
        "date_obtention",
        "date_expiration",
        "ordre",
    )
    search_fields = ("nom", "organisme", "identifiant", "description")
    autocomplete_fields = ("profil", "badge")
    filter_horizontal = ("competences",)
    list_editable = ("ordre",)
    ordering = ("-date_obtention", "ordre")
    date_hierarchy = "date_obtention"

    fieldsets = (
        ("Identification", {"fields": ("profil", "nom", "organisme", "ordre")}),
        (
            "Dates",
            {"fields": ("date_obtention", "date_expiration")},
        ),
        (
            "Détails",
            {"fields": ("identifiant", "url_verification", "description", "badge")},
        ),
        ("Compétences", {"fields": ("competences",)}),
    )