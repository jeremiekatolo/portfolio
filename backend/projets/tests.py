"""
Tests unitaires et API pour l'app projets.
"""

from datetime import date, timedelta

from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from categories.models import Categorie
from competences.models import Competence
from technologies.models import Technologie
from utilisateurs.models import Utilisateur

from .models import Projet


class ProjetModelTest(TestCase):
    def setUp(self):
        self.user = Utilisateur.objects.create_user(
            username="auteur", password="pass1234567890"
        )
        self.cat = Categorie.objects.create(
            nom="Réseau", type=Categorie.TypeChoices.PROJET
        )

    def test_slug_auto_generated(self):
        p = Projet.objects.create(
            titre="Segmentation réseau",
            categorie=self.cat,
            auteur=self.user,
        )
        self.assertEqual(p.slug, "segmentation-reseau")

    def test_slug_unique(self):
        Projet.objects.create(
            titre="Test", categorie=self.cat, auteur=self.user
        )
        p2 = Projet.objects.create(
            titre="Test", categorie=self.cat, auteur=self.user
        )
        self.assertEqual(p2.slug, "test-2")

    def test_statut_default_brouillon(self):
        p = Projet.objects.create(
            titre="X", categorie=self.cat, auteur=self.user
        )
        self.assertEqual(p.statut, Projet.StatutChoices.BROUILLON)

    def test_est_public_false_si_brouillon(self):
        p = Projet.objects.create(
            titre="X", categorie=self.cat, auteur=self.user
        )
        self.assertFalse(p.est_public)

    def test_est_public_true_si_publie(self):
        p = Projet.objects.create(
            titre="X",
            categorie=self.cat,
            auteur=self.user,
            statut=Projet.StatutChoices.PUBLIE,
        )
        self.assertTrue(p.est_public)

    def test_est_public_false_si_publish_at_futur(self):
        p = Projet.objects.create(
            titre="X",
            categorie=self.cat,
            auteur=self.user,
            statut=Projet.StatutChoices.PUBLIE,
            publish_at=timezone.now() + timedelta(days=1),
        )
        self.assertFalse(p.est_public)

    def test_manager_publies(self):
        Projet.objects.create(
            titre="Brouillon", categorie=self.cat, auteur=self.user
        )
        Projet.objects.create(
            titre="Publié",
            categorie=self.cat,
            auteur=self.user,
            statut=Projet.StatutChoices.PUBLIE,
        )
        self.assertEqual(Projet.objects.publies().count(), 1)


class ProjetAPITest(TestCase):
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
        self.tech = Technologie.objects.create(nom="Django")
        self.comp = Competence.objects.create(
            nom="TCP/IP", domaine=Competence.DomaineChoices.RESEAUX
        )
        self.projet_public = Projet.objects.create(
            titre="Public",
            categorie=self.cat,
            auteur=self.admin,
            statut=Projet.StatutChoices.PUBLIE,
        )
        self.projet_brouillon = Projet.objects.create(
            titre="Brouillon",
            categorie=self.cat,
            auteur=self.admin,
            statut=Projet.StatutChoices.BROUILLON,
        )

    def test_visiteur_ne_voit_que_les_projets_publies(self):
        response = self.client.get("/api/projets/projets/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        items = response.data.get("results", response.data)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["titre"], "Public")

    def test_visiteur_ne_peut_pas_acceder_au_brouillon_par_slug(self):
        response = self.client.get(
            f"/api/projets/projets/{self.projet_brouillon.slug}/"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_editeur_voit_tous_les_projets(self):
        self.client.force_authenticate(user=self.editeur)
        response = self.client.get("/api/projets/projets/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        items = response.data.get("results", response.data)
        self.assertEqual(len(items), 2)

    def test_creation_refusee_anonyme(self):
        response = self.client.post(
            "/api/projets/projets/",
            {"titre": "Nouveau", "categorie_id": self.cat.pk},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_creation_par_editeur(self):
        self.client.force_authenticate(user=self.editeur)
        response = self.client.post(
            "/api/projets/projets/",
            {
                "titre": "Nouveau projet",
                "categorie_id": self.cat.pk,
                "difficulte": "avance",
                "technologies_ids": [self.tech.pk],
                "competences_ids": [self.comp.pk],
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Vérifie que les M2M sont bien liés.
        projet = Projet.objects.get(slug="nouveau-projet")
        self.assertEqual(projet.technologies.count(), 1)
        self.assertEqual(projet.competences.count(), 1)