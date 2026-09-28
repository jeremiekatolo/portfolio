"""
Tests unitaires pour l'app categories.
"""

from django.db import IntegrityError
from django.test import TestCase

from .models import Categorie


class CategorieModelTest(TestCase):
    def test_slug_auto_generated_from_nom(self):
        cat = Categorie.objects.create(nom="Réseau et Sécurité", type=Categorie.TypeChoices.PROJET)
        self.assertEqual(cat.slug, "reseau-et-securite")

    def test_slug_unique_par_type(self):
        """Vérifie que le slug reste unique par type grâce au suffixe automatique."""
        cat1 = Categorie.objects.create(
            nom="Réseau", type=Categorie.TypeChoices.PROJET
        )
        self.assertEqual(cat1.slug, "reseau")

        # Même slug, autre type → OK
        cat2 = Categorie.objects.create(
            nom="Réseau", type=Categorie.TypeChoices.LABORATOIRE
        )
        self.assertEqual(cat2.slug, "reseau")

        # Même slug, même type → suffixe automatique -2
        cat3 = Categorie.objects.create(
            nom="Réseau", type=Categorie.TypeChoices.PROJET
        )
        self.assertEqual(cat3.slug, "reseau-2")

    def test_unique_constraint_enforced_at_db_level(self):
        """
        Vérifie que la contrainte unique (type, slug) existe bien en base,
        même si on contourne le save() via .update().
        """
        cat1 = Categorie.objects.create(
            nom="Test", type=Categorie.TypeChoices.PROJET
        )
        cat2 = Categorie.objects.create(
            nom="Autre", type=Categorie.TypeChoices.PROJET
        )
        # Force le slug identique via update() — contourne save()
        with self.assertRaises(IntegrityError):
            Categorie.objects.filter(pk=cat2.pk).update(slug=cat1.slug)

    def test_slug_collision_gets_suffix(self):
        Categorie.objects.create(nom="Test", type=Categorie.TypeChoices.PROJET)
        cat2 = Categorie.objects.create(nom="Test", type=Categorie.TypeChoices.PROJET)
        self.assertEqual(cat2.slug, "test-2")

    def test_slug_respects_manual_value(self):
        cat = Categorie.objects.create(
            nom="Peu importe", slug="mon-slug-custom", type=Categorie.TypeChoices.ARTICLE
        )
        self.assertEqual(cat.slug, "mon-slug-custom")

    def test_str_includes_type_and_nom(self):
        cat = Categorie.objects.create(nom="Cybersécurité", type=Categorie.TypeChoices.PROJET)
        self.assertIn("Cybersécurité", str(cat))
        self.assertIn("Projet", str(cat))