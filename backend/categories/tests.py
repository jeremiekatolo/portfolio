"""
Tests unitaires et API pour l'app categories.
"""

from django.db import IntegrityError
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from utilisateurs.models import Utilisateur
from .models import Categorie


# ---------------------------------------------------------------------------
# Tests modèles
# ---------------------------------------------------------------------------


class CategorieModelTest(TestCase):
    def test_slug_auto_generated_from_nom(self):
        cat = Categorie.objects.create(
            nom="Réseau et Sécurité", type=Categorie.TypeChoices.PROJET
        )
        self.assertEqual(cat.slug, "reseau-et-securite")

    def test_slug_unique_par_type(self):
        cat1 = Categorie.objects.create(
            nom="Réseau", type=Categorie.TypeChoices.PROJET
        )
        self.assertEqual(cat1.slug, "reseau")

        cat2 = Categorie.objects.create(
            nom="Réseau", type=Categorie.TypeChoices.LABORATOIRE
        )
        self.assertEqual(cat2.slug, "reseau")

        cat3 = Categorie.objects.create(
            nom="Réseau", type=Categorie.TypeChoices.PROJET
        )
        self.assertEqual(cat3.slug, "reseau-2")

    def test_unique_constraint_enforced_at_db_level(self):
        cat1 = Categorie.objects.create(
            nom="Test", type=Categorie.TypeChoices.PROJET
        )
        cat2 = Categorie.objects.create(
            nom="Autre", type=Categorie.TypeChoices.PROJET
        )
        with self.assertRaises(IntegrityError):
            Categorie.objects.filter(pk=cat2.pk).update(slug=cat1.slug)

    def test_slug_respects_manual_value(self):
        cat = Categorie.objects.create(
            nom="Peu importe",
            slug="mon-slug-custom",
            type=Categorie.TypeChoices.ARTICLE,
        )
        self.assertEqual(cat.slug, "mon-slug-custom")

    def test_str_includes_type_and_nom(self):
        cat = Categorie.objects.create(
            nom="Cybersécurité", type=Categorie.TypeChoices.PROJET
        )
        self.assertIn("Cybersécurité", str(cat))
        self.assertIn("Projet", str(cat))


# ---------------------------------------------------------------------------
# Tests API
# ---------------------------------------------------------------------------


class CategorieAPITest(TestCase):
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
        self.cat = Categorie.objects.create(
            nom="Réseau", type=Categorie.TypeChoices.PROJET
        )

    def test_liste_publique(self):
        response = self.client.get("/api/categories/categories/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_public(self):
        response = self.client.get(f"/api/categories/categories/{self.cat.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nom"], "Réseau")

    def test_creation_refusee_anonyme(self):
        response = self.client.post(
            "/api/categories/categories/",
            {"nom": "Test", "type": "projet"},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_creation_refusee_visiteur(self):
        self.client.force_authenticate(user=self.visiteur)
        response = self.client.post(
            "/api/categories/categories/",
            {"nom": "Test", "type": "projet"},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_creation_par_editeur(self):
        self.client.force_authenticate(user=self.editeur)
        response = self.client.post(
            "/api/categories/categories/",
            {"nom": "Nouveau réseau", "type": "projet"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["slug"], "nouveau-reseau")

    def test_slug_genere_si_non_fourni(self):
        self.client.force_authenticate(user=self.editeur)
        response = self.client.post(
            "/api/categories/categories/",
            {"nom": "Réseau avancé", "type": "laboratoire"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["slug"], "reseau-avance")

    def test_filtre_par_type(self):
        Categorie.objects.create(
            nom="Article réseau", type=Categorie.TypeChoices.ARTICLE
        )
        response = self.client.get("/api/categories/categories/?type=projet")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Selon la pagination, résultats dans 'results'.
        items = response.data.get("results", response.data)
        self.assertTrue(all(item["type"] == "projet" for item in items))