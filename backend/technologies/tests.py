"""
Tests unitaires pour l'app technologies.
"""

from django.db import IntegrityError
from django.test import TestCase

from .models import Technologie


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