"""
Tests unitaires et API pour l'app technologies.
"""

from django.db import IntegrityError
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from utilisateurs.models import Utilisateur
from .models import Technologie


# ---------------------------------------------------------------------------
# Tests modèles
# ---------------------------------------------------------------------------


class TechnologieModelTest(TestCase):
    def test_create_minimal(self):
        tech = Technologie.objects.create(nom="Django")
        self.assertEqual(tech.nom, "Django")
        self.assertEqual(tech.categorie_tech, Technologie.CategorieTechChoices.AUTRE)

    def test_nom_unique(self):
        Technologie.objects.create(nom="Docker")
        with self.assertRaises(IntegrityError):
            Technologie.objects.create(nom="Docker")

    def test_str_returns_nom(self):
        tech = Technologie.objects.create(nom="Kubernetes")
        self.assertEqual(str(tech), "Kubernetes")

    def test_categorie_tech_choices(self):
        tech = Technologie.objects.create(
            nom="Nginx", categorie_tech=Technologie.CategorieTechChoices.OUTIL
        )
        self.assertEqual(tech.categorie_tech, "outil")


# ---------------------------------------------------------------------------
# Tests API
# ---------------------------------------------------------------------------


class TechnologieAPITest(TestCase):
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
        self.tech = Technologie.objects.create(
            nom="Django", categorie_tech=Technologie.CategorieTechChoices.BACKEND
        )

    def test_liste_publique(self):
        response = self.client.get("/api/technologies/technologies/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_public(self):
        response = self.client.get(
            f"/api/technologies/technologies/{self.tech.pk}/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nom"], "Django")

    def test_creation_refusee_anonyme(self):
        response = self.client.post(
            "/api/technologies/technologies/",
            {"nom": "Nouveau", "categorie_tech": "backend"},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_creation_refusee_visiteur(self):
        self.client.force_authenticate(user=self.visiteur)
        response = self.client.post(
            "/api/technologies/technologies/",
            {"nom": "Nouveau", "categorie_tech": "backend"},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_creation_par_editeur(self):
        self.client.force_authenticate(user=self.editeur)
        response = self.client.post(
            "/api/technologies/technologies/",
            {"nom": "PostgreSQL", "categorie_tech": "database"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["nom"], "PostgreSQL")

    def test_creation_refusee_doublon(self):
        self.client.force_authenticate(user=self.editeur)
        response = self.client.post(
            "/api/technologies/technologies/",
            {"nom": "Django", "categorie_tech": "backend"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filtre_par_categorie(self):
        Technologie.objects.create(
            nom="PostgreSQL", categorie_tech=Technologie.CategorieTechChoices.DATABASE
        )
        response = self.client.get(
            "/api/technologies/technologies/?categorie_tech=backend"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        items = response.data.get("results", response.data)
        self.assertTrue(all(item["categorie_tech"] == "backend" for item in items))