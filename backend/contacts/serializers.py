"""
Serializers DRF pour l'app contacts.

Deux serializers :
- ContactPublicSerializer : création (POST public), sans exposition de l'ip_hash.
- ContactAdminSerializer  : lecture/modification (réservé à l'admin), avec tous les champs.
"""

from rest_framework import serializers

from .models import Contact


class ContactPublicSerializer(serializers.ModelSerializer):
    """
    Serializer utilisé pour la création publique.

    Sécurité :
    - `ip_hash` et `user_agent` sont remplis côté serveur dans la vue.
    - `statut` est forcé à `nouveau`.
    - Honeypot : champ optionnel `website` qui doit rester vide.
    """

    # Honeypot invisible côté frontend. S'il est rempli → spam.
    website = serializers.CharField(
        required=False, allow_blank=True, write_only=True
    )

    class Meta:
        model = Contact
        fields = (
            "id",
            "nom",
            "email",
            "sujet",
            "message",
            "website",  # honeypot
            "date_envoi",
        )
        read_only_fields = ("id", "date_envoi")

    def validate_message(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError(
                "Le message doit contenir au moins 10 caractères."
            )
        return value

    def validate_nom(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError(
                "Le nom doit contenir au moins 2 caractères."
            )
        return value

    def validate(self, attrs):
        # Honeypot : si le champ `website` est rempli, on rejette silencieusement.
        if attrs.get("website"):
            raise serializers.ValidationError(
                {"detail": "Requête rejetée."}
            )
        return attrs


class ContactAdminSerializer(serializers.ModelSerializer):
    """Serializer complet réservé à l’administration."""

    statut_display = serializers.CharField(
        source="get_statut_display", read_only=True
    )

    class Meta:
        model = Contact
        fields = (
            "id",
            "nom",
            "email",
            "sujet",
            "message",
            "date_envoi",
            "ip_hash",
            "user_agent",
            "statut",
            "statut_display",
        )
        read_only_fields = (
            "id",
            "nom",
            "email",
            "sujet",
            "message",
            "date_envoi",
            "ip_hash",
            "user_agent",
        )