"""
Tests unitaires et API pour l'app utilisateurs.

Deux groupes :
- Tests modèles (comportement Django pur).
- Tests API (via DRF APIClient).
"""

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import Profil

Utilisateur = get_user_model()


# ---------------------------------------------------------------------------
# Tests modèles
# ---------------------------------------------------------------------------


class UtilisateurModelTest(TestCase):
    def test_create_user_default_role_is_visiteur(self):
        user = Utilisateur.objects.create_user(
            username="testuser", password="testpass123456"
        )
        self.assertEqual(user.role, Utilisateur.Role.VISITEUR)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        user = Utilisateur.objects.create_superuser(
            username="admin", password="testpass123456"
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_str_returns_username(self):
        user = Utilisateur.objects.create_user(
            username="testuser", password="testpass123456"
        )
        self.assertEqual(str(user), "testuser")


class ProfilModelTest(TestCase):
    def setUp(self):
        self.user = Utilisateur.objects.create_user(
            username="testuser", password="testpass123456"
        )

    def test_str_returns_username(self):
        profil = Profil.objects.create(utilisateur=self.user)
        self.assertEqual(str(profil), "Profil de testuser")

    def test_one_to_one_constraint(self):
        Profil.objects.create(utilisateur=self.user)
        with self.assertRaises(IntegrityError):
            Profil.objects.create(utilisateur=self.user)


# ---------------------------------------------------------------------------
# Tests API
# ---------------------------------------------------------------------------


class UtilisateurAPITest(TestCase):
    """Tests de l'API Utilisateur."""

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

    def test_liste_publique(self):
        """Tout le monde peut lire la liste."""
        response = self.client.get("/api/utilisateurs/utilisateurs/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_creation_refusee_si_non_authentifie(self):
        """Un anonyme ne peut pas créer."""
        response = self.client.post(
            "/api/utilisateurs/utilisateurs/",
            {
                "username": "nouveau",
                "email": "n@example.com",
                "password": "MotDePasse!2026",
                "password_confirm": "MotDePasse!2026",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_creation_refusee_si_role_visiteur(self):
        """Un visiteur authentifié ne peut pas créer."""
        self.client.force_authenticate(user=self.visiteur)
        response = self.client.post(
            "/api/utilisateurs/utilisateurs/",
            {
                "username": "nouveau",
                "email": "n@example.com",
                "password": "MotDePasse!2026",
                "password_confirm": "MotDePasse!2026",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_creation_par_editeur(self):
        """Un éditeur peut créer un utilisateur."""
        self.client.force_authenticate(user=self.editeur)
        response = self.client.post(
            "/api/utilisateurs/utilisateurs/",
            {
                "username": "nouveau",
                "email": "n@example.com",
                "password": "MotDePasse!2026",
                "password_confirm": "MotDePasse!2026",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Utilisateur.objects.filter(username="nouveau").exists()
        )

    def test_creation_refusee_si_mots_de_passe_differents(self):
        """Les deux mots de passe doivent correspondre."""
        self.client.force_authenticate(user=self.editeur)
        response = self.client.post(
            "/api/utilisateurs/utilisateurs/",
            {
                "username": "nouveau",
                "password": "MotDePasse!2026",
                "password_confirm": "AutreMotDePasse!2026",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password_confirm", response.data)

    def test_creation_refusee_si_mot_de_passe_absent(self):
        """Le mot de passe est obligatoire à la création."""
        self.client.force_authenticate(user=self.editeur)
        response = self.client.post(
            "/api/utilisateurs/utilisateurs/",
            {"username": "nouveau"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_password_jamais_renvoye_en_lecture(self):
        """Le mot de passe n'est jamais dans la réponse."""
        response = self.client.get("/api/utilisateurs/utilisateurs/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Selon la pagination, les résultats sont dans 'results'.
        for user_data in response.data.get("results", []):
            self.assertNotIn("password", user_data)
            self.assertNotIn("password_confirm", user_data)

    def test_me_requires_authentication(self):
        """`/moi/` exige une authentification."""
        response = self.client.get("/api/utilisateurs/moi/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_me_returns_current_user(self):
        """`/moi/` retourne l'utilisateur connecté."""
        self.client.force_authenticate(user=self.editeur)
        response = self.client.get("/api/utilisateurs/moi/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "editeur")


class ProfilAPITest(TestCase):
    """Tests de l'API Profil."""

    def setUp(self):
        self.client = APIClient()
        self.admin = Utilisateur.objects.create_superuser(
            username="admin", password="adminpass123456"
        )
        self.user = Utilisateur.objects.create_user(
            username="user", password="userpass123456"
        )
        self.profil = Profil.objects.create(
            utilisateur=self.user, nom_public="Jean Test"
        )

    def test_liste_publique(self):
        response = self.client.get("/api/utilisateurs/profils/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_public(self):
        response = self.client.get(
            f"/api/utilisateurs/profils/{self.profil.pk}/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nom_public"], "Jean Test")

    def test_modification_refusee_pour_visiteur(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            f"/api/utilisateurs/profils/{self.profil.pk}/",
            {"nom_public": "Nouveau nom"},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)