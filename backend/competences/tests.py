"""
Tests unitaires et API pour l'app competences.
"""

from django.db import IntegrityError
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from utilisateurs.models import Utilisateur
from .models import Competence


# ---------------------------------------------------------------------------
# Tests modèles
# ---------------------------------------------------------------------------


class CompetenceModelTest(TestCase):
    def test_create_minimal(self):
        comp = Competence.objects.create(
            nom="TCP/IP", domaine=Competence.DomaineChoices.RESEAUX
        )
        self.assertEqual(comp.domaine, "reseaux")

    def test_nom_unique(self):
        Competence.objects.create(
            nom="Linux", domaine=Competence.DomaineChoices.SYSTEMES
        )
        with self.assertRaises(IntegrityError):
            Competence.objects.create(
                nom="Linux", domaine=Competence.DomaineChoices.CYBERSECURITE
            )

    def test_no_percentage_field(self):
        """Règle métier : aucun champ pourcentage ou niveau."""
        champs = [f.name for f in Competence._meta.get_fields()]
        for interdit in ("pourcentage", "niveau", "score", "rating"):
            self.assertNotIn(interdit, champs)

    def test_str_includes_domaine_and_nom(self):
        comp = Competence.objects.create(
            nom="TLS", domaine=Competence.DomaineChoices.CYBERSECURITE
        )
        self.assertIn("TLS", str(comp))
        self.assertIn("Cybersécurité", str(comp))


# ---------------------------------------------------------------------------
# Tests API
# ---------------------------------------------------------------------------


class CompetenceAPITest(TestCase):
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
        self.comp = Competence.objects.create(
            nom="TCP/IP", domaine=Competence.DomaineChoices.RESEAUX
        )

    def test_liste_publique(self):
        response = self.client.get("/api/competences/competences/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_public(self):
        response = self.client.get(
            f"/api/competences/competences/{self.comp.pk}/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nom"], "TCP/IP")

    def test_creation_refusee_anonyme(self):
        response = self.client.post(
            "/api/competences/competences/",
            {"nom": "Nouvelle", "domaine": "reseaux"},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_creation_refusee_visiteur(self):
        self.client.force_authenticate(user=self.visiteur)
        response = self.client.post(
            "/api/competences/competences/",
            {"nom": "Nouvelle", "domaine": "reseaux"},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_creation_par_editeur(self):
        self.client.force_authenticate(user=self.editeur)
        response = self.client.post(
            "/api/competences/competences/",
            {"nom": "VLAN", "domaine": "reseaux"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["nom"], "VLAN")

    def test_creation_refusee_doublon(self):
        self.client.force_authenticate(user=self.editeur)
        response = self.client.post(
            "/api/competences/competences/",
            {"nom": "TCP/IP", "domaine": "cybersecurite"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filtre_par_domaine(self):
        Competence.objects.create(
            nom="TLS", domaine=Competence.DomaineChoices.CYBERSECURITE
        )
        response = self.client.get(
            "/api/competences/competences/?domaine=reseaux"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        items = response.data.get("results", response.data)
        self.assertTrue(all(item["domaine"] == "reseaux" for item in items))

    def test_reponse_ne_contient_pas_de_pourcentage(self):
        """La réponse API ne doit jamais contenir de champ pourcentage/niveau."""
        response = self.client.get("/api/competences/competences/")
        for item in response.data.get("results", []):
            for interdit in ("pourcentage", "niveau", "score"):
                self.assertNotIn(interdit, item)