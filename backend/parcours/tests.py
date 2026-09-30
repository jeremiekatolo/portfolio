"""
Tests unitaires et API pour l'app parcours.
"""

from datetime import date

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from competences.models import Competence
from utilisateurs.models import Profil, Utilisateur

from .models import Certification, Parcours


class ParcoursModelTest(TestCase):
    def setUp(self):
        self.user = Utilisateur.objects.create_user(
            username="owner", password="pass1234567890"
        )
        self.profil = Profil.objects.create(utilisateur=self.user)
        self.comp = Competence.objects.create(
            nom="TCP/IP", domaine=Competence.DomaineChoices.RESEAUX
        )

    def test_create_parcours(self):
        p = Parcours.objects.create(
            profil=self.profil,
            titre="Ingénieur Réseau",
            type=Parcours.TypeChoices.EXPERIENCE,
            date_debut=date(2020, 1, 1),
        )
        self.assertEqual(p.get_type_display(), "Expérience professionnelle")
        self.assertTrue(p.est_en_cours)

    def test_str_includes_titre_and_type(self):
        p = Parcours.objects.create(
            profil=self.profil,
            titre="Master Réseaux",
            type=Parcours.TypeChoices.FORMATION,
            date_debut=date(2018, 9, 1),
            date_fin=date(2020, 6, 30),
        )
        self.assertIn("Master Réseaux", str(p))
        self.assertIn("Formation", str(p))
        self.assertFalse(p.est_en_cours)

    def test_m2m_competences(self):
        p = Parcours.objects.create(
            profil=self.profil,
            titre="X",
            type=Parcours.TypeChoices.EXPERIENCE,
            date_debut=date(2020, 1, 1),
        )
        p.competences.add(self.comp)
        self.assertEqual(p.competences.count(), 1)


class CertificationModelTest(TestCase):
    def setUp(self):
        self.user = Utilisateur.objects.create_user(
            username="owner", password="pass1234567890"
        )
        self.profil = Profil.objects.create(utilisateur=self.user)

    def test_create_certification(self):
        c = Certification.objects.create(
            profil=self.profil,
            nom="CCNA",
            organisme="Cisco",
            date_obtention=date(2023, 5, 1),
        )
        self.assertEqual(str(c), "CCNA")

    def test_est_expiree_false_si_pas_d_expiration(self):
        c = Certification.objects.create(
            profil=self.profil,
            nom="X",
            date_obtention=date(2023, 1, 1),
        )
        self.assertFalse(c.est_expiree)

    def test_est_expiree_true_si_date_passee(self):
        c = Certification.objects.create(
            profil=self.profil,
            nom="X",
            date_obtention=date(2018, 1, 1),
            date_expiration=date(2020, 1, 1),
        )
        self.assertTrue(c.est_expiree)


class ParcoursAPITest(TestCase):
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
        self.profil = Profil.objects.create(utilisateur=self.admin)
        self.comp = Competence.objects.create(
            nom="VLAN", domaine=Competence.DomaineChoices.RESEAUX
        )
        self.parcours = Parcours.objects.create(
            profil=self.profil,
            titre="Ingénieur",
            type=Parcours.TypeChoices.EXPERIENCE,
            date_debut=date(2020, 1, 1),
        )

    def test_liste_publique(self):
        response = self.client.get("/api/parcours/parcours/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_creation_refusee_anonyme(self):
        response = self.client.post(
            "/api/parcours/parcours/",
            {
                "profil_id": self.profil.pk,
                "titre": "X",
                "type": "experience",
                "date_debut": "2020-01-01",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_creation_par_editeur(self):
        self.client.force_authenticate(user=self.editeur)
        response = self.client.post(
            "/api/parcours/parcours/",
            {
                "profil_id": self.profil.pk,
                "titre": "Nouveau poste",
                "type": "experience",
                "date_debut": "2022-01-01",
                "competences_ids": [self.comp.pk],
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        p = Parcours.objects.get(titre="Nouveau poste")
        self.assertEqual(p.competences.count(), 1)

    def test_date_fin_avant_debut_refusee(self):
        self.client.force_authenticate(user=self.editeur)
        response = self.client.post(
            "/api/parcours/parcours/",
            {
                "profil_id": self.profil.pk,
                "titre": "X",
                "type": "experience",
                "date_debut": "2022-01-01",
                "date_fin": "2020-01-01",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CertificationAPITest(TestCase):
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
        self.profil = Profil.objects.create(utilisateur=self.admin)
        self.cert = Certification.objects.create(
            profil=self.profil,
            nom="CCNA",
            date_obtention=date(2023, 5, 1),
        )

    def test_liste_publique(self):
        response = self.client.get("/api/parcours/certifications/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_creation_refusee_anonyme(self):
        response = self.client.post(
            "/api/parcours/certifications/",
            {
                "profil_id": self.profil.pk,
                "nom": "X",
                "date_obtention": "2023-01-01",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_creation_par_editeur(self):
        self.client.force_authenticate(user=self.editeur)
        response = self.client.post(
            "/api/parcours/certifications/",
            {
                "profil_id": self.profil.pk,
                "nom": "CompTIA Security+",
                "date_obtention": "2024-01-01",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)