"""
Tests unitaires minimaux pour l'app utilisateurs.

Objectif : vérifier le comportement de base des modèles.
Les tests complets (permissions, API, etc.) viendront plus tard.
"""

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

from .models import Profil


class UtilisateurModelTest(TestCase):
    def test_create_user_default_role_is_visiteur(self):
        Utilisateur = get_user_model()
        user = Utilisateur.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.assertEqual(user.role, Utilisateur.Role.VISITEUR)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        Utilisateur = get_user_model()
        user = Utilisateur.objects.create_superuser(
            username="admin", password="testpass123"
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_str_returns_username(self):
        Utilisateur = get_user_model()
        user = Utilisateur.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.assertEqual(str(user), "testuser")


class ProfilModelTest(TestCase):
    def setUp(self):
        Utilisateur = get_user_model()
        self.user = Utilisateur.objects.create_user(
            username="testuser", password="testpass123"
        )

    def test_str_returns_username(self):
        profil = Profil.objects.create(utilisateur=self.user)
        self.assertEqual(str(profil), "Profil de testuser")

    def test_one_to_one_constraint(self):
        Profil.objects.create(utilisateur=self.user)
        with self.assertRaises(IntegrityError):
            Profil.objects.create(utilisateur=self.user)