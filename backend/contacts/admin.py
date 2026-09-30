"""
Admin Django pour l'app contacts.

- Tous les champs sont en lecture seule sauf `statut`.
- Actions : marquer comme lu, traité, spam.
"""

from django.contrib import admin

from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "nom",
        "email",
        "sujet",
        "date_envoi",
        "statut",
    )
    list_filter = ("statut", "date_envoi")
    search_fields = ("nom", "email", "sujet", "message")
    readonly_fields = (
        "nom",
        "email",
        "sujet",
        "message",
        "date_envoi",
        "ip_hash",
        "user_agent",
    )
    date_hierarchy = "date_envoi"
    ordering = ("-date_envoi",)
    actions = ("marquer_comme_lu", "marquer_comme_traite", "marquer_comme_spam")

    fieldsets = (
        ("Expéditeur", {"fields": ("nom", "email")}),
        ("Message", {"fields": ("sujet", "message")}),
        (
            "Métadonnées",
            {
                "fields": ("date_envoi", "ip_hash", "user_agent"),
                "classes": ("collapse",),
            },
        ),
        ("Traitement", {"fields": ("statut",)}),
    )

    @admin.action(description="Marquer comme lu")
    def marquer_comme_lu(self, request, queryset):
        queryset.update(statut=Contact.StatutChoices.LU)

    @admin.action(description="Marquer comme traité")
    def marquer_comme_traite(self, request, queryset):
        queryset.update(statut=Contact.StatutChoices.TRAITE)

    @admin.action(description="Marquer comme spam")
    def marquer_comme_spam(self, request, queryset):
        queryset.update(statut=Contact.StatutChoices.SPAM)