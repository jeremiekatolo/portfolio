"""
Admin Django pour l'app audits.

Lecture seule stricte : aucune création, modification ou suppression
manuelle. La purge se fera via une commande dédiée (Phase 6+).
"""

from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = (
        "date",
        "utilisateur",
        "action",
        "resultat",
        "content_type",
        "object_id",
    )
    list_filter = ("action", "resultat", "content_type", "date")
    search_fields = ("utilisateur__username", "metadonnees")
    readonly_fields = (
        "utilisateur",
        "action",
        "content_type",
        "object_id",
        "date",
        "ip_hash",
        "resultat",
        "metadonnees",
    )
    date_hierarchy = "date"
    ordering = ("-date",)

    # Interdit toute création, modification ou suppression.
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    fieldsets = (
        ("Qui", {"fields": ("utilisateur",)}),
        ("Quoi", {"fields": ("action", "resultat")}),
        (
            "Sur quoi",
            {"fields": ("content_type", "object_id")},
        ),
        ("Quand", {"fields": ("date", "ip_hash")}),
        ("Métadonnées", {"fields": ("metadonnees",)}),
    )