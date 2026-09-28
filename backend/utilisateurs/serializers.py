"""
Serializers DRF pour l'app utilisateurs.

- UtilisateurSerializer : lecture/écriture du modèle Utilisateur.
  Le mot de passe est en write_only, avec confirmation obligatoire
  (password + password_confirm), haché via set_password().
- ProfilSerializer : profil complet avec URLs des médias (photo, cv, seo_image).
- MeSerializer : vue « moi » pour l'utilisateur connecté (avec profil imbriqué).
"""

from django.contrib.auth import get_user_model
from rest_framework import serializers

from medias.models import Media
from .models import Profil

Utilisateur = get_user_model()


class UtilisateurSerializer(serializers.ModelSerializer):
    """
    Serializer Utilisateur avec gestion sécurisée du mot de passe.

    Règles :
    - À la création : `password` et `password_confirm` sont obligatoires.
    - À la mise à jour : si `password` est fourni, `password_confirm` doit
      l'être aussi, et les deux doivent être identiques.
    - Le mot de passe n'est jamais renvoyé en lecture.
    """

    password = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=False,
        min_length=12,
        style={"input_type": "password"},
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=False,
        style={"input_type": "password"},
    )
    role_display = serializers.CharField(source="get_role_display", read_only=True)

    class Meta:
        model = Utilisateur
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "role_display",
            "is_active",
            "is_staff",
            "date_joined",
            "last_login",
            "password",
            "password_confirm",
        )
        read_only_fields = ("id", "date_joined", "last_login", "is_staff")

    # ------------------------------------------------------------------
    # Validation globale (à la création ET à la mise à jour)
    # ------------------------------------------------------------------

    def validate(self, attrs):
        """
        Vérifie la cohérence entre `password` et `password_confirm`.

        À la création (self.instance is None) : les deux sont obligatoires.
        À la mise à jour : les deux doivent être fournis ensemble (ou aucun).
        """
        password = attrs.get("password")
        password_confirm = attrs.get("password_confirm")

        if self.instance is None:
            # Création : les deux champs sont obligatoires.
            if not password:
                raise serializers.ValidationError(
                    {"password": "Le mot de passe est obligatoire à la création."}
                )
            if not password_confirm:
                raise serializers.ValidationError(
                    {
                        "password_confirm": (
                            "La confirmation du mot de passe est obligatoire."
                        )
                    }
                )
        else:
            # Mise à jour : si l'un est fourni, l'autre doit l'être aussi.
            if password and not password_confirm:
                raise serializers.ValidationError(
                    {
                        "password_confirm": (
                            "Veuillez confirmer le nouveau mot de passe."
                        )
                    }
                )
            if password_confirm and not password:
                raise serializers.ValidationError(
                    {
                        "password": (
                            "Veuillez saisir le nouveau mot de passe."
                        )
                    }
                )

        if password and password_confirm and password != password_confirm:
            raise serializers.ValidationError(
                {"password_confirm": "Les deux mots de passe ne correspondent pas."}
            )

        return attrs

    # ------------------------------------------------------------------
    # Create / Update
    # ------------------------------------------------------------------

    def create(self, validated_data):
        # On retire `password_confirm` : ce n'est pas un champ du modèle.
        validated_data.pop("password_confirm", None)
        password = validated_data.pop("password", None)

        user = Utilisateur(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

    def update(self, instance, validated_data):
        validated_data.pop("password_confirm", None)
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class MediaInlineSerializer(serializers.Serializer):
    """Représentation minimale d'un média lié."""

    id = serializers.IntegerField(read_only=True)
    fichier = serializers.FileField(read_only=True)
    alt_text = serializers.CharField(read_only=True)
    type = serializers.CharField(read_only=True)


class ProfilSerializer(serializers.ModelSerializer):
    """Serializer Profil avec médias imbriqués en lecture seule."""

    utilisateur_username = serializers.CharField(
        source="utilisateur.username", read_only=True
    )
    photo = MediaInlineSerializer(read_only=True)
    cv = MediaInlineSerializer(read_only=True)
    seo_image_defaut = MediaInlineSerializer(read_only=True)

    photo_id = serializers.PrimaryKeyRelatedField(
        source="photo",
        queryset=Media.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )
    cv_id = serializers.PrimaryKeyRelatedField(
        source="cv",
        queryset=Media.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )
    seo_image_defaut_id = serializers.PrimaryKeyRelatedField(
        source="seo_image_defaut",
        queryset=Media.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Profil
        fields = (
            "id",
            "utilisateur",
            "utilisateur_username",
            "nom_public",
            "titre_principal",
            "titre_secondaire",
            "bio_courte",
            "bio_longue",
            "email_public",
            "telephone_public",
            "localisation",
            "photo",
            "photo_id",
            "cv",
            "cv_id",
            "disponible",
            "seo_titre_defaut",
            "seo_description_defaut",
            "seo_image_defaut",
            "seo_image_defaut_id",
            "date_creation",
            "date_modification",
        )
        read_only_fields = ("id", "date_creation", "date_modification")


class MeSerializer(serializers.ModelSerializer):
    """Vue « moi » : Utilisateur + Profil imbriqué (lecture seule)."""

    profil = ProfilSerializer(read_only=True)
    role_display = serializers.CharField(source="get_role_display", read_only=True)

    class Meta:
        model = Utilisateur
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "role_display",
            "is_superuser",
            "is_staff",
            "is_active",
            "profil",
        )
        read_only_fields = fields