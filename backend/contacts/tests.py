"""
Tests unitaires et API pour l'app contacts.
"""

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from utilisateurs.models import Utilisateur

from .models import Contact


class ContactModelTest(TestCase):
    def test_create_contact(self):
        c = Contact.objects.create(
            nom="Jean",
            email="jean@example.com",
            sujet="Question",
            message="Bonjour, j'aimerais en savoir plus.",
        )
        self.assertEqual(c.statut, Contact.StatutChoices.NOUVEAU)
        self.assertIn("Jean", str(c))

    def test_hash_ip(self):
        h = Contact.hasher_ip("192.168.1.1")
        self.assertEqual(len(h), 64)  # SHA-256 = 64 hex chars

    def test_hash_ip_empty(self):
        self.assertEqual(Contact.hasher_ip(""), "")


class ContactAPITest(TestCase):
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
        self.contact = Contact.objects.create(
            nom="Jean",
            email="jean@example.com",
            sujet="Question",
            message="Bonjour, j'aimerais en savoir plus.",
        )

    def test_creation_publique_autorisee(self):
        """Le POST est public — un visiteur peut envoyer un message."""
        response = self.client.post(
            "/api/contacts/contacts/",
            {
                "nom": "Marie",
                "email": "marie@example.com",
                "sujet": "Devis",
                "message": "Je souhaite un devis pour un audit.",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        c = Contact.objects.get(nom="Marie")
        self.assertEqual(c.statut, Contact.StatutChoices.NOUVEAU)
        # Vérifie que ip_hash est renseigné côté serveur.
        self.assertEqual(len(c.ip_hash), 64)

    def test_honeypot_bloque_spam(self):
        """Un bot qui remplit le honeypot est rejeté."""
        response = self.client.post(
            "/api/contacts/contacts/",
            {
                "nom": "Bot",
                "email": "bot@spam.com",
                "sujet": "Spam",
                "message": "Achetez nos produits à prix réduit !",
                "website": "http://spam.example.com",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_message_trop_court_refuse(self):
        response = self.client.post(
            "/api/contacts/contacts/",
            {
                "nom": "Marie",
                "email": "marie@example.com",
                "sujet": "Court",
                "message": "Court",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_liste_refusee_anonyme(self):
        """La liste des messages est privée."""
        response = self.client.get("/api/contacts/contacts/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_liste_refusee_editeur(self):
        """Même un éditeur ne peut pas lire les messages."""
        self.client.force_authenticate(user=self.editeur)
        response = self.client.get("/api/contacts/contacts/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_liste_accessible_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get("/api/contacts/contacts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_modification_statut_par_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(
            f"/api/contacts/contacts/{self.contact.pk}/",
            {"statut": "traite"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.statut, Contact.StatutChoices.TRAITE)

    def test_modification_statut_refusee_editeur(self):
        self.client.force_authenticate(user=self.editeur)
        response = self.client.patch(
            f"/api/contacts/contacts/{self.contact.pk}/",
            {"statut": "traite"},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_suppression_refusee_editeur(self):
        self.client.force_authenticate(user=self.editeur)
        response = self.client.delete(f"/api/contacts/contacts/{self.contact.pk}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_suppression_autorisee_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(f"/api/contacts/contacts/{self.contact.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)