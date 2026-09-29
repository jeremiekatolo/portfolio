"""
Tests unitaires et API pour l'app medias.
"""

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import LienExterne, Media, MediaLien

Utilisateur = get_user_model()


class MediaModelTest(TestCase):
    def test_create_media_computes_metadata(self):
        fichier = SimpleUploadedFile(
            "mon-schema.png", b"contenu binaire factice", content_type="image/png"
        )
        media = Media.objects.create(fichier=fichier, type=Media.TypeChoices.SCHEMA)
        self.assertEqual(media.nom_original, "mon-schema.png")
        self.assertGreater(media.taille, 0)
        self.assertEqual(len(media.hash_sha256), 64)

    def test_default_type_is_autre(self):
        media = Media.objects.create(fichier=SimpleUploadedFile("x.bin", b"abc"))
        self.assertEqual(media.type, Media.TypeChoices.AUTRE)


class MediaLienModelTest(TestCase):
    def setUp(self):
        self.media = Media.objects.create(
            fichier=SimpleUploadedFile("img.png", b"contenu")
        )
        self.user = Utilisateur.objects.create_user(
            username="testuser", password="testpass123456"
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


class LienExterneModelTest(TestCase):
    def setUp(self):
        self.user = Utilisateur.objects.create_user(
            username="testuser", password="testpass123456"
        )

    def test_create_lien_externe(self):
        ct = ContentType.objects.get_for_model(self.user)
        lien = LienExterne.objects.create(
            content_type=ct,
            object_id=self.user.pk,
            type=LienExterne.TypeChoices.GITHUB,
            url="https://github.com/exemple/repo",
        )
        self.assertEqual(lien.content_object, self.user)


class MediaAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.editeur = Utilisateur.objects.create_user(
            username="editeur",
            password="editeurpass123456",
            role=Utilisateur.Role.EDITEUR,
        )
        self.visiteur = Utilisateur.objects.create_user(
            username="visiteur", password="visiteurpass123456"
        )

    def test_liste_publique(self):
        response = self.client.get("/api/medias/medias/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_upload_refuse_anonyme(self):
        fichier = SimpleUploadedFile("img.png", b"abc", content_type="image/png")
        response = self.client.post(
            "/api/medias/medias/", {"fichier": fichier, "type": "image"}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_upload_par_editeur(self):
        self.client.force_authenticate(user=self.editeur)
        fichier = SimpleUploadedFile("img.png", b"abc", content_type="image/png")
        response = self.client.post(
            "/api/medias/medias/",
            {"fichier": fichier, "type": "image"},
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["uploaded_by"], self.editeur.pk)