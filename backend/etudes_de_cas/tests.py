"""
Tests unitaires et API pour l'app etudes_de_cas.
"""

from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from competences.models import Competence
from technologies.models import Technologie
from utilisateurs.models import Utilisateur

from .models import EtudeDeCas


class EtudeDeCasModelTest(TestCase):
    def setUp(self):
        self.user = Utilisateur.objects.create_user(
            username="auteur", password="pass1234567890"
        )

    def test_slug_auto_generated(self):
        e = EtudeDeCas.objects.create(
            titre="Durcissement d'un pare-feu", auteur=self.user
        )
        self.assertEqual(e.slug, "durcissement-dun-pare-feu")

    def test_slug_unique(self):
        EtudeDeCas.objects.create(titre="Test", auteur=self.user)
        e2 = EtudeDeCas.objects.create(titre="Test", auteur=self.user)
        self.assertEqual(e2.slug, "test-2")

    def test_statut_default_brouillon(self):
        e = EtudeDeCas.objects.create(titre="X", auteur=self.user)
        self.assertEqual(e.statut, EtudeDeCas.StatutChoices.BROUILLON)

    def test_est_public_false_si_brouillon(self):
        e = EtudeDeCas.objects.create(titre="X", auteur=self.user)
        self.assertFalse(e.est_public)

    def test_est_public_true_si_publie(self):
        e = EtudeDeCas.objects.create(
            titre="X",
            auteur=self.user,
            statut=EtudeDeCas.StatutChoices.PUBLIE,
        )
        self.assertTrue(e.est_public)

    def test_est_public_false_si_publish_at_futur(self):
        e = EtudeDeCas.objects.create(
            titre="X",
            auteur=self.user,
            statut=EtudeDeCas.StatutChoices.PUBLIE,
            publish_at=timezone.now() + timedelta(days=1),
        )
        self.assertFalse(e.est_public)

    def test_manager_publies(self):
        EtudeDeCas.objects.create(titre="Brouillon", auteur=self.user)
        EtudeDeCas.objects.create(
            titre="Publié",
            auteur=self.user,
            statut=EtudeDeCas.StatutChoices.PUBLIE,
        )
        self.assertEqual(EtudeDeCas.objects.publies().count(), 1)


class EtudeDeCasAPITest(TestCase):
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
        self.tech = Technologie.objects.create(nom="pfSense")
        self.comp = Competence.objects.create(
            nom="Firewall", domaine=Competence.DomaineChoices.CYBERSECURITE
        )
        self.etude_public = EtudeDeCas.objects.create(
            titre="Public",
            auteur=self.admin,
            statut=EtudeDeCas.StatutChoices.PUBLIE,
        )
        self.etude_brouillon = EtudeDeCas.objects.create(
            titre="Brouillon",
            auteur=self.admin,
            statut=EtudeDeCas.StatutChoices.BROUILLON,
        )

    def test_visiteur_ne_voit_que_les_etudes_publiees(self):
        response = self.client.get("/api/etudes-de-cas/etudes-de-cas/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        items = response.data.get("results", response.data)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["titre"], "Public")

    def test_visiteur_ne_peut_pas_acceder_au_brouillon(self):
        response = self.client.get(
            f"/api/etudes-de-cas/etudes-de-cas/{self.etude_brouillon.slug}/"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_editeur_voit_toutes_les_etudes(self):
        self.client.force_authenticate(user=self.editeur)
        response = self.client.get("/api/etudes-de-cas/etudes-de-cas/")
        items = response.data.get("results", response.data)
        self.assertEqual(len(items), 2)

    def test_creation_refusee_anonyme(self):
        response = self.client.post(
            "/api/etudes-de-cas/etudes-de-cas/", {"titre": "Nouvelle"}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_creation_par_editeur(self):
        self.client.force_authenticate(user=self.editeur)
        response = self.client.post(
            "/api/etudes-de-cas/etudes-de-cas/",
            {
                "titre": "Analyse incident",
                "probleme": "Détection tardive",
                "technologies_ids": [self.tech.pk],
                "competences_ids": [self.comp.pk],
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        etude = EtudeDeCas.objects.get(slug="analyse-incident")
        self.assertEqual(etude.technologies.count(), 1)
        self.assertEqual(etude.competences.count(), 1)