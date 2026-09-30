"""
Tests unitaires et API pour l'app audits.
"""

from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from categories.models import Categorie
from utilisateurs.models import Utilisateur

from .models import AuditLog
from .services import journaliser


class AuditLogModelTest(TestCase):
    def setUp(self):
        self.user = Utilisateur.objects.create_user(
            username="testuser", password="pass1234567890"
        )

    def test_create_log(self):
        log = AuditLog.objects.create(
            utilisateur=self.user,
            action=AuditLog.ActionChoices.LOGIN_SUCCESS,
        )
        self.assertEqual(log.action, "login_success")
        self.assertEqual(log.resultat, AuditLog.ResultatChoices.SUCCES)

    def test_hash_ip(self):
        h = AuditLog.hasher_ip("192.168.1.1")
        self.assertEqual(len(h), 64)

    def test_hash_ip_empty(self):
        self.assertEqual(AuditLog.hasher_ip(""), "")

    def test_str_includes_username_and_action(self):
        log = AuditLog.objects.create(
            utilisateur=self.user,
            action=AuditLog.ActionChoices.LOGIN_SUCCESS,
        )
        self.assertIn("testuser", str(log))
        self.assertIn("Connexion réussie", str(log))

    def test_immuable_apres_creation(self):
        log = AuditLog.objects.create(
            utilisateur=self.user,
            action=AuditLog.ActionChoices.LOGIN_SUCCESS,
        )
        log.action = AuditLog.ActionChoices.LOGIN_FAILED
        with self.assertRaises(ValueError):
            log.save()

    def test_suppression_interdite(self):
        log = AuditLog.objects.create(
            utilisateur=self.user,
            action=AuditLog.ActionChoices.LOGIN_SUCCESS,
        )
        with self.assertRaises(ValueError):
            log.delete()

    def test_content_object_generic(self):
        cat = Categorie.objects.create(
            nom="Test", type=Categorie.TypeChoices.PROJET
        )
        log = AuditLog.objects.create(
            utilisateur=self.user,
            action=AuditLog.ActionChoices.CONTENT_CREATED,
            content_type=ContentType.objects.get_for_model(cat),
            object_id=cat.pk,
        )
        self.assertEqual(log.content_object, cat)


class JournaliserServiceTest(TestCase):
    def setUp(self):
        self.user = Utilisateur.objects.create_user(
            username="testuser", password="pass1234567890"
        )

    def test_journaliser_creation(self):
        log = journaliser(
            utilisateur=self.user,
            action=AuditLog.ActionChoices.LOGIN_SUCCESS,
        )
        self.assertIsNotNone(log)
        self.assertEqual(AuditLog.objects.count(), 1)

    def test_journaliser_sans_utilisateur(self):
        log = journaliser(
            action=AuditLog.ActionChoices.OTHER,
        )
        self.assertIsNotNone(log)
        self.assertIsNone(log.utilisateur)


class AuditLogAPITest(TestCase):
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
        self.log = AuditLog.objects.create(
            utilisateur=self.admin,
            action=AuditLog.ActionChoices.LOGIN_SUCCESS,
        )

    def test_liste_refusee_anonyme(self):
        response = self.client.get("/api/audits/logs/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_liste_refusee_editeur(self):
        self.client.force_authenticate(user=self.editeur)
        response = self.client.get("/api/audits/logs/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_liste_accessible_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get("/api/audits/logs/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_creation_refusee_meme_pour_admin(self):
        """Aucune création via l'API — même pour un admin."""
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            "/api/audits/logs/",
            {"action": "other"},
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_suppression_refusee_meme_pour_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(f"/api/audits/logs/{self.log.pk}/")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_filtre_par_action(self):
        self.client.force_authenticate(user=self.admin)
        AuditLog.objects.create(
            utilisateur=self.admin,
            action=AuditLog.ActionChoices.LOGIN_FAILED,
        )
        response = self.client.get("/api/audits/logs/?action=login_success")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        items = response.data.get("results", response.data)
        self.assertEqual(len(items), 1)