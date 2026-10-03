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

from django.contrib.contenttypes.models import ContentType
from medias.models import LienExterne

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

class ProjetWorkflowAPITest(TestCase):
    """Tests des actions de workflow de publication."""

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
        self.projet = Projet.objects.create(
            titre="Workflow Test",
            categorie=self.cat,
            auteur=self.admin,
            statut=Projet.StatutChoices.BROUILLON,
        )

    def _url(self, action: str) -> str:
        return f"/api/projets/projets/{self.projet.slug}/{action}/"

    # --- Soumettre ---

    def test_soumettre_refuse_anonyme(self):
        response = self.client.post(self._url("soumettre"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_soumettre_refuse_visiteur(self):
        self.client.force_authenticate(user=self.visiteur)
        response = self.client.post(self._url("soumettre"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_soumettre_autorise_editeur(self):
        self.client.force_authenticate(user=self.editeur)
        response = self.client.post(self._url("soumettre"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.projet.refresh_from_db()
        self.assertEqual(self.projet.statut, Projet.StatutChoices.EN_REVISION)

    def test_soumettre_refuse_si_deja_en_revision(self):
        self.projet.statut = Projet.StatutChoices.EN_REVISION
        self.projet.save()
        self.client.force_authenticate(user=self.editeur)
        response = self.client.post(self._url("soumettre"))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # --- Valider ---

    def test_valider_refuse_editeur(self):
        self.projet.statut = Projet.StatutChoices.EN_REVISION
        self.projet.save()
        self.client.force_authenticate(user=self.editeur)
        response = self.client.post(self._url("valider"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_valider_autorise_admin(self):
        self.projet.statut = Projet.StatutChoices.EN_REVISION
        self.projet.save()
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self._url("valider"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.projet.refresh_from_db()
        self.assertEqual(self.projet.statut, Projet.StatutChoices.VALIDE)

    # --- Publier ---

    def test_publier_refuse_editeur(self):
        self.client.force_authenticate(user=self.editeur)
        response = self.client.post(self._url("publier"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_publier_autorise_admin_depuis_brouillon(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self._url("publier"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.projet.refresh_from_db()
        self.assertEqual(self.projet.statut, Projet.StatutChoices.PUBLIE)

    def test_publier_refuse_si_deja_publie(self):
        self.projet.statut = Projet.StatutChoices.PUBLIE
        self.projet.save()
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self._url("publier"))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # --- Dépublier ---

    def test_depublier_autorise_admin(self):
        self.projet.statut = Projet.StatutChoices.PUBLIE
        self.projet.save()
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self._url("depublier"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.projet.refresh_from_db()
        self.assertEqual(self.projet.statut, Projet.StatutChoices.BROUILLON)

    def test_depublier_refuse_si_pas_publie(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self._url("depublier"))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # --- Archiver ---

    def test_archiver_autorise_admin_depuis_publie(self):
        self.projet.statut = Projet.StatutChoices.PUBLIE
        self.projet.save()
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self._url("archiver"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.projet.refresh_from_db()
        self.assertEqual(self.projet.statut, Projet.StatutChoices.ARCHIVE)

    def test_archiver_refuse_depuis_brouillon(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self._url("archiver"))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)       

class ProjetLiensExternesAPITest(TestCase):
    """Vérifie que les liens externes sont exposés par l'API."""

    def setUp(self):
        self.client = APIClient()
        self.admin = Utilisateur.objects.create_superuser(
            username="admin", password="adminpass123456"
        )
        self.cat = Categorie.objects.create(
            nom="Réseau", type=Categorie.TypeChoices.PROJET
        )
        self.projet = Projet.objects.create(
            titre="Avec liens",
            categorie=self.cat,
            auteur=self.admin,
            statut=Projet.StatutChoices.PUBLIE,
        )
        # Crée 2 liens externes liés au projet
        ct = ContentType.objects.get_for_model(self.projet)
        LienExterne.objects.create(
            content_type=ct,
            object_id=self.projet.pk,
            type=LienExterne.TypeChoices.GITHUB,
            url="https://github.com/exemple/repo",
            label="Code source",
            ordre=1,
        )
        LienExterne.objects.create(
            content_type=ct,
            object_id=self.projet.pk,
            type=LienExterne.TypeChoices.DEMO,
            url="https://demo.exemple.com",
            label="Démo en ligne",
            ordre=2,
        )

    def test_liens_externes_exposes(self):
        response = self.client.get(
            f"/api/projets/projets/{self.projet.slug}/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        liens = response.data["liens_externes"]
        self.assertEqual(len(liens), 2)
        self.assertEqual(liens[0]["type"], "github")
        self.assertEqual(liens[0]["url"], "https://github.com/exemple/repo")
        self.assertEqual(liens[0]["type_display"], "GitHub")
        self.assertEqual(liens[1]["type"], "demo")

    def test_projet_sans_liens(self):
        projet2 = Projet.objects.create(
            titre="Sans liens",
            categorie=self.cat,
            auteur=self.admin,
            statut=Projet.StatutChoices.PUBLIE,
        )
        response = self.client.get(
            f"/api/projets/projets/{projet2.slug}/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["liens_externes"], [])