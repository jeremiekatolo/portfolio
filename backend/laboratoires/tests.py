"""
Tests unitaires et API pour l'app laboratoires.
"""

from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from competences.models import Competence
from technologies.models import Technologie
from utilisateurs.models import Utilisateur

from .models import Laboratoire


class LaboratoireModelTest(TestCase):
    def setUp(self):
        self.user = Utilisateur.objects.create_user(
            username="auteur", password="pass1234567890"
        )

    def test_slug_auto_generated(self):
        lab = Laboratoire.objects.create(
            titre="Linux Hardening", auteur=self.user
        )
        self.assertEqual(lab.slug, "linux-hardening")

    def test_slug_unique(self):
        Laboratoire.objects.create(titre="Test", auteur=self.user)
        lab2 = Laboratoire.objects.create(titre="Test", auteur=self.user)
        self.assertEqual(lab2.slug, "test-2")

    def test_statut_default_brouillon(self):
        lab = Laboratoire.objects.create(titre="X", auteur=self.user)
        self.assertEqual(lab.statut, Laboratoire.StatutChoices.BROUILLON)

    def test_est_public_false_si_brouillon(self):
        lab = Laboratoire.objects.create(titre="X", auteur=self.user)
        self.assertFalse(lab.est_public)

    def test_est_public_true_si_publie(self):
        lab = Laboratoire.objects.create(
            titre="X",
            auteur=self.user,
            statut=Laboratoire.StatutChoices.PUBLIE,
        )
        self.assertTrue(lab.est_public)

    def test_est_public_false_si_publish_at_futur(self):
        lab = Laboratoire.objects.create(
            titre="X",
            auteur=self.user,
            statut=Laboratoire.StatutChoices.PUBLIE,
            publish_at=timezone.now() + timedelta(days=1),
        )
        self.assertFalse(lab.est_public)

    def test_manager_publies(self):
        Laboratoire.objects.create(titre="Brouillon", auteur=self.user)
        Laboratoire.objects.create(
            titre="Publié",
            auteur=self.user,
            statut=Laboratoire.StatutChoices.PUBLIE,
        )
        self.assertEqual(Laboratoire.objects.publies().count(), 1)


class LaboratoireAPITest(TestCase):
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
        self.tech = Technologie.objects.create(nom="Wireshark")
        self.comp = Competence.objects.create(
            nom="Analyse réseau", domaine=Competence.DomaineChoices.RESEAUX
        )
        self.lab_public = Laboratoire.objects.create(
            titre="Public",
            auteur=self.admin,
            statut=Laboratoire.StatutChoices.PUBLIE,
        )
        self.lab_brouillon = Laboratoire.objects.create(
            titre="Brouillon",
            auteur=self.admin,
            statut=Laboratoire.StatutChoices.BROUILLON,
        )

    def test_visiteur_ne_voit_que_les_labos_publies(self):
        response = self.client.get("/api/laboratoires/laboratoires/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        items = response.data.get("results", response.data)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["titre"], "Public")

    def test_visiteur_ne_peut_pas_acceder_au_brouillon(self):
        response = self.client.get(
            f"/api/laboratoires/laboratoires/{self.lab_brouillon.slug}/"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_editeur_voit_tous_les_labos(self):
        self.client.force_authenticate(user=self.editeur)
        response = self.client.get("/api/laboratoires/laboratoires/")
        items = response.data.get("results", response.data)
        self.assertEqual(len(items), 2)

    def test_creation_refusee_anonyme(self):
        response = self.client.post(
            "/api/laboratoires/laboratoires/", {"titre": "Nouveau"}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_creation_par_editeur(self):
        self.client.force_authenticate(user=self.editeur)
        response = self.client.post(
            "/api/laboratoires/laboratoires/",
            {
                "titre": "Analyse pcap",
                "objectif": "Détecter du trafic malveillant",
                "difficulte": "avance",
                "technologies_ids": [self.tech.pk],
                "competences_ids": [self.comp.pk],
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        lab = Laboratoire.objects.get(slug="analyse-pcap")
        self.assertEqual(lab.technologies.count(), 1)
        self.assertEqual(lab.competences.count(), 1)

class LaboratoireWorkflowAPITest(TestCase):
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
        self.labo = Laboratoire.objects.create(
            titre="Workflow Test",
            auteur=self.admin,
            statut=Laboratoire.StatutChoices.BROUILLON,
        )

    def _url(self, action: str) -> str:
        return f"/api/laboratoires/laboratoires/{self.labo.slug}/{action}/"

    def test_soumettre_refuse_anonyme(self):
        response = self.client.post(self._url("soumettre"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_soumettre_autorise_editeur(self):
        self.client.force_authenticate(user=self.editeur)
        response = self.client.post(self._url("soumettre"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.labo.refresh_from_db()
        self.assertEqual(self.labo.statut, Laboratoire.StatutChoices.EN_REVISION)

    def test_soumettre_refuse_si_deja_en_revision(self):
        self.labo.statut = Laboratoire.StatutChoices.EN_REVISION
        self.labo.save()
        self.client.force_authenticate(user=self.editeur)
        response = self.client.post(self._url("soumettre"))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valider_refuse_editeur(self):
        self.labo.statut = Laboratoire.StatutChoices.EN_REVISION
        self.labo.save()
        self.client.force_authenticate(user=self.editeur)
        response = self.client.post(self._url("valider"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_valider_autorise_admin(self):
        self.labo.statut = Laboratoire.StatutChoices.EN_REVISION
        self.labo.save()
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self._url("valider"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.labo.refresh_from_db()
        self.assertEqual(self.labo.statut, Laboratoire.StatutChoices.VALIDE)

    def test_publier_autorise_admin_depuis_brouillon(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self._url("publier"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.labo.refresh_from_db()
        self.assertEqual(self.labo.statut, Laboratoire.StatutChoices.PUBLIE)

    def test_publier_refuse_editeur(self):
        self.client.force_authenticate(user=self.editeur)
        response = self.client.post(self._url("publier"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_depublier_autorise_admin(self):
        self.labo.statut = Laboratoire.StatutChoices.PUBLIE
        self.labo.save()
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self._url("depublier"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.labo.refresh_from_db()
        self.assertEqual(self.labo.statut, Laboratoire.StatutChoices.BROUILLON)

    def test_depublier_refuse_si_pas_publie(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self._url("depublier"))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_archiver_autorise_admin_depuis_publie(self):
        self.labo.statut = Laboratoire.StatutChoices.PUBLIE
        self.labo.save()
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self._url("archiver"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.labo.refresh_from_db()
        self.assertEqual(self.labo.statut, Laboratoire.StatutChoices.ARCHIVE)

    def test_archiver_refuse_depuis_brouillon(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self._url("archiver"))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)