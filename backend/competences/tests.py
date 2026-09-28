"""
Tests unitaires pour l'app competences.
"""

from django.db import IntegrityError
from django.test import TestCase

from .models import Competence


class CompetenceModelTest(TestCase):
    def test_create_minimal(self):
        comp = Competence.objects.create(nom="TCP/IP", domaine=Competence.DomaineChoices.RESEAUX)
        self.assertEqual(comp.domaine, "reseaux")

    def test_nom_unique(self):
        Competence.objects.create(nom="Linux", domaine=Competence.DomaineChoices.SYSTEMES)
        with self.assertRaises(IntegrityError):
            Competence.objects.create(nom="Linux", domaine=Competence.DomaineChoices.CYBERSECURITE)

    def test_no_percentage_field(self):
        """Règle métier : aucun champ pourcentage ou niveau."""
        champs = [f.name for f in Competence._meta.get_fields()]
        for interdit in ("pourcentage", "niveau", "score", "rating"):
            self.assertNotIn(interdit, champs)

    def test_str_includes_domaine_and_nom(self):
        comp = Competence.objects.create(nom="TLS", domaine=Competence.DomaineChoices.CYBERSECURITE)
        self.assertIn("TLS", str(comp))
        self.assertIn("Cybersécurité", str(comp))