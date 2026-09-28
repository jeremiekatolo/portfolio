"""
Tests unitaires minimaux pour l'app medias.

Objectif :
- Vérifier le comportement des 3 modèles.
- Vérifier le calcul automatique des métadonnées du Media.
- Vérifier la liaison polymorphe MediaLien / LienExterne.

Les tests d'upload réel (avec un vrai fichier) et les validations
de sécurité (taille, MIME, extension) viendront en Phase 6.
"""

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from .models import LienExterne, Media, MediaLien


class MediaModelTest(TestCase):
    """Tests du modèle Media."""

    def test_create_media_computes_metadata(self):
        """Le save() doit calculer nom_original, taille et hash_sha256."""
        fichier = SimpleUploadedFile(
            "mon-schema.png",
            b"contenu binaire factice",
            content_type="image/png",
        )
        media = Media.objects.create(
            fichier=fichier,
            type=Media.TypeChoices.SCHEMA,
        )
        self.assertEqual(media.nom_original, "mon-schema.png")
        self.assertGreater(media.taille, 0)
        self.assertEqual(len(media.hash_sha256), 64)  # SHA-256 = 64 hex chars
        self.assertEqual(media.type, Media.TypeChoices.SCHEMA)

    def test_hash_is_unique_for_same_content(self):
        """Deux uploads du même contenu → même hash → contrainte unique."""
        fichier1 = SimpleUploadedFile(
            "a.png", b"identique", content_type="image/png"
        )
        fichier2 = SimpleUploadedFile(
            "b.png", b"identique", content_type="image/png"
        )
        Media.objects.create(fichier=fichier1)
        with self.assertRaises(Exception):
            # Le hash SHA-256 est unique : la 2e insertion doit échouer.
            Media.objects.create(fichier=fichier2)

    def test_default_type_is_autre(self):
        fichier = SimpleUploadedFile("x.bin", b"abc")
        media = Media.objects.create(fichier=fichier)
        self.assertEqual(media.type, Media.TypeChoices.AUTRE)

    def test_default_est_orphelin_is_false(self):
        fichier = SimpleUploadedFile("x.bin", b"abc")
        media = Media.objects.create(fichier=fichier)
        self.assertFalse(media.est_orphelin)


class MediaLienModelTest(TestCase):
    """Tests du modèle MediaLien (liaison polymorphe)."""

    def setUp(self):
        self.fichier = SimpleUploadedFile("img.png", b"contenu")
        self.media = Media.objects.create(fichier=self.fichier)
        # On utilise Utilisateur comme objet polymorphe de test
        # (n'importe quel modèle Django ferait l'affaire).
        Utilisateur = get_user_model()
        self.user = Utilisateur.objects.create_user(
            username="testuser", password="testpass123"
        )

    def test_create_lien_polymorphe(self):
        ct = ContentType.objects.get_for_model(self.user)
        lien = MediaLien.objects.create(
            media=self.media,
            content_type=ct,
            object_id=self.user.pk,
            role=MediaLien.RoleChoices.COUVERTURE,
        )
        self.assertEqual(lien.content_object, self.user)
        self.assertEqual(lien.role, MediaLien.RoleChoices.COUVERTURE)

    def test_default_role_is_illustration(self):
        ct = ContentType.objects.get_for_model(self.user)
        lien = MediaLien.objects.create(
            media=self.media,
            content_type=ct,
            object_id=self.user.pk,
        )
        self.assertEqual(lien.role, MediaLien.RoleChoices.ILLUSTRATION)


class LienExterneModelTest(TestCase):
    """Tests du modèle LienExterne (liaison polymorphe)."""

    def setUp(self):
        Utilisateur = get_user_model()
        self.user = Utilisateur.objects.create_user(
            username="testuser", password="testpass123"
        )

    def test_create_lien_externe(self):
        ct = ContentType.objects.get_for_model(self.user)
        lien = LienExterne.objects.create(
            content_type=ct,
            object_id=self.user.pk,
            type=LienExterne.TypeChoices.GITHUB,
            url="https://github.com/exemple/repo",
            label="Dépôt GitHub",
        )
        self.assertEqual(lien.content_object, self.user)
        self.assertEqual(lien.type, LienExterne.TypeChoices.GITHUB)

    def test_default_type_is_autre(self):
        ct = ContentType.objects.get_for_model(self.user)
        lien = LienExterne.objects.create(
            content_type=ct,
            object_id=self.user.pk,
            url="https://example.com",
        )
        self.assertEqual(lien.type, LienExterne.TypeChoices.AUTRE)

    def test_str_returns_type_and_url(self):
        ct = ContentType.objects.get_for_model(self.user)
        lien = LienExterne.objects.create(
            content_type=ct,
            object_id=self.user.pk,
            type=LienExterne.TypeChoices.DEMO,
            url="https://demo.example.com",
        )
        self.assertEqual(str(lien), "Démonstration — https://demo.example.com")