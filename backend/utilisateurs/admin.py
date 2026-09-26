"""
Configuration de l'admin Django pour l'app utilisateurs.

- Utilisateur : étend UserAdmin standard avec le champ `role`.
- Profil      : ModelAdmin simple, organisé en sections.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import Profil, Utilisateur


@admin.register(Utilisateur)
class UtilisateurAdmin(DjangoUserAdmin):
    """Admin du modèle Utilisateur custom."""

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "role",
        "is_staff",
        "is_active",
    )
    list_filter = ("role", "is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username",)

    # Ajoute `role` aux fieldsets standards de Django.
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Portfolio", {"fields": ("role",)}),
    )
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        ("Portfolio", {"fields": ("role",)}),
    )


@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    """Admin du modèle Profil."""

    list_display = (
        "utilisateur",
        "nom_public",
        "titre_principal",
        "disponible",
        "date_modification",
    )
    list_filter = ("disponible",)
    search_fields = ("utilisateur__username", "nom_public", "titre_principal")
    readonly_fields = ("date_creation", "date_modification")
    autocomplete_fields = ("utilisateur",)

    fieldsets = (
        ("Utilisateur", {"fields": ("utilisateur",)}),
        (
            "Identité publique",
            {
                "fields": (
                    "nom_public",
                    "titre_principal",
                    "titre_secondaire",
                    "bio_courte",
                    "bio_longue",
                )
            },
        ),
        (
            "Contact public",
            {"fields": ("email_public", "telephone_public", "localisation")},
        ),
        ("Disponibilité", {"fields": ("disponible",)}),
        (
            "SEO par défaut",
            {"fields": ("seo_titre_defaut", "seo_description_defaut")},
        ),
        (
            "Horodatage",
            {
                "fields": ("date_creation", "date_modification"),
                "classes": ("collapse",),
            },
        ),
    )