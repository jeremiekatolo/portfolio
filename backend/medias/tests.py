"""
Tests unitaires et API pour l'app medias.

Deux groupes :
- Tests modèles (calcul du hash, liaison polymorphe).
- Tests API (upload, permissions, liaison polymorphe).
"""

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import LienExterne, Media, MediaLien

Utilisateur = get_user_model()


# ---------------------------------------------------------------------------
# Tests modèles
# ---------------------------------------------------------------------------


class MediaModelTest(TestCase):
    def test_create_media_computes_metadata(self):
        fichier = SimpleUploadedFile(
            "mon-schema.png",
            b"contenu binaire factice",
            content_type="image/png",
        )
        media = Media.objects.create(
            fichier=fichier, type=Media.TypeChoices.SCHEMA
        )
        self.assertEqual(media.nom_original, "mon-schema.png")
        self.assertGreater(media.taille, 0)
        self.assertEqual(len(media.hash_sha256), 64)
        self.assertEqual(media.type, Media.TypeChoices.SCHEMA)

    def test_default_type_is_autre(self):
        media = Media.objects.create(
            fichier=SimpleUploadedFile("x.bin", b"abc")
        )
        self.assertEqual(media.type, Media.TypeChoices.AUTRE)

    def test_default_est_orphelin_is_false(self):
        media = Media.objects.create(
            fichier=SimpleUploadedFile("x.bin", b"abc")
        )
        self.assertFalse(media.est_orphelin)


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

    def test_default_role_is_illustration(self):
        ct = ContentType.objects.get_for_model(self.user)
        lien = MediaLien.objects.create(
            media=self.media, content_type=ct, object_id=self.user.pk
        )
        self.assertEqual(lien.role, MediaLien.RoleChoices.ILLUSTRATION)


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

    def test_default_type_is_autre(self):
        ct = ContentType.objects.get_for_model(self.user)
        lien = LienExterne.objects.create(
            content_type=ct,
            object_id=self.user.pk,
            url="https://example.com",
        )
        self.assertEqual(lien.type, LienExterne.TypeChoices.AUTRE)


# ---------------------------------------------------------------------------
# Tests API
# ---------------------------------------------------------------------------


class MediaAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = Utilisateur.objects.create_superuser(
            username="admin", password="adminpass123456"
        )
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

    def test_upload_refuse_visiteur(self):
        self.client.force_authenticate(user=self.visiteur)
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
        self.assertEqual(response.data["nom_original"], "img.png")
        self.assertEqual(response.data["uploaded_by"], self.editeur.pk)

    def test_password_jamais_dans_reponse(self):
        """Le serializer Media n'a pas de champ password (vérif. de bon sens)."""
        response = self.client.get("/api/medias/medias/")
        for item in response.data.get("results", []):
            self.assertNotIn("password", item)


class LienExterneAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = Utilisateur.objects.create_superuser(
            username="admin", password="adminpass123456"
        )
        self.user = Utilisateur.objects.create_user(
            username="user", password="userpass123456"
        )
        self.ct = ContentType.objects.get_for_model(self.user)

    def test_liste_publique(self):
        response = self.client.get("/api/medias/liens-externes/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_creation_refusee_visiteur(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            "/api/medias/liens-externes/",
            {
                "content_type": self.ct.pk,
                "object_id": self.user.pk,
                "type": "github",
                "url": "https://github.com/x/y",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_creation_par_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            "/api/medias/liens-externes/",
            {
                "content_type": self.ct.pk,
                "object_id": self.user.pk,
                "type": "github",
                "url": "https://github.com/x/y",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)