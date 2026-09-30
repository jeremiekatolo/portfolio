"""
Tests unitaires et API pour l'app articles.
"""

from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from categories.models import Categorie
from competences.models import Competence
from technologies.models import Technologie
from utilisateurs.models import Utilisateur

from .models import Article


class ArticleModelTest(TestCase):
    def setUp(self):
        self.user = Utilisateur.objects.create_user(
            username="auteur", password="pass1234567890"
        )
        self.cat = Categorie.objects.create(
            nom="Réseau", type=Categorie.TypeChoices.ARTICLE
        )

    def test_slug_auto_generated(self):
        a = Article.objects.create(
            titre="Sécuriser une API DRF",
            categorie=self.cat,
            auteur=self.user,
        )
        self.assertEqual(a.slug, "securiser-une-api-drf")

    def test_slug_unique(self):
        Article.objects.create(
            titre="Test", categorie=self.cat, auteur=self.user
        )
        a2 = Article.objects.create(
            titre="Test", categorie=self.cat, auteur=self.user
        )
        self.assertEqual(a2.slug, "test-2")

    def test_statut_default_brouillon(self):
        a = Article.objects.create(
            titre="X", categorie=self.cat, auteur=self.user
        )
        self.assertEqual(a.statut, Article.StatutChoices.BROUILLON)

    def test_est_public_false_si_brouillon(self):
        a = Article.objects.create(
            titre="X", categorie=self.cat, auteur=self.user
        )
        self.assertFalse(a.est_public)

    def test_est_public_true_si_publie(self):
        a = Article.objects.create(
            titre="X",
            categorie=self.cat,
            auteur=self.user,
            statut=Article.StatutChoices.PUBLIE,
        )
        self.assertTrue(a.est_public)

    def test_est_public_false_si_publish_at_futur(self):
        a = Article.objects.create(
            titre="X",
            categorie=self.cat,
            auteur=self.user,
            statut=Article.StatutChoices.PUBLIE,
            publish_at=timezone.now() + timedelta(days=1),
        )
        self.assertFalse(a.est_public)

    def test_manager_publies(self):
        Article.objects.create(
            titre="Brouillon", categorie=self.cat, auteur=self.user
        )
        Article.objects.create(
            titre="Publié",
            categorie=self.cat,
            auteur=self.user,
            statut=Article.StatutChoices.PUBLIE,
        )
        self.assertEqual(Article.objects.publies().count(), 1)

    def test_temps_lecture_calcule(self):
        contenu = "mot " * 400  # 400 mots → ~2 minutes
        a = Article.objects.create(
            titre="Test lecture",
            categorie=self.cat,
            auteur=self.user,
            contenu=contenu,
        )
        self.assertEqual(a.temps_lecture, 2)


class ArticleAPITest(TestCase):
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
            nom="Cybersécurité", type=Categorie.TypeChoices.ARTICLE
        )
        self.tech = Technologie.objects.create(nom="DRF")
        self.comp = Competence.objects.create(
            nom="API Security", domaine=Competence.DomaineChoices.CYBERSECURITE
        )
        self.art_public = Article.objects.create(
            titre="Public",
            categorie=self.cat,
            auteur=self.admin,
            statut=Article.StatutChoices.PUBLIE,
        )
        self.art_brouillon = Article.objects.create(
            titre="Brouillon",
            categorie=self.cat,
            auteur=self.admin,
            statut=Article.StatutChoices.BROUILLON,
        )

    def test_visiteur_ne_voit_que_les_articles_publies(self):
        response = self.client.get("/api/articles/articles/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        items = response.data.get("results", response.data)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["titre"], "Public")

    def test_visiteur_ne_peut_pas_acceder_au_brouillon(self):
        response = self.client.get(
            f"/api/articles/articles/{self.art_brouillon.slug}/"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_editeur_voit_tous_les_articles(self):
        self.client.force_authenticate(user=self.editeur)
        response = self.client.get("/api/articles/articles/")
        items = response.data.get("results", response.data)
        self.assertEqual(len(items), 2)

    def test_creation_refusee_anonyme(self):
        response = self.client.post(
            "/api/articles/articles/",
            {"titre": "Nouveau", "categorie_id": self.cat.pk},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_creation_par_editeur(self):
        self.client.force_authenticate(user=self.editeur)
        response = self.client.post(
            "/api/articles/articles/",
            {
                "titre": "Nouvel article",
                "categorie_id": self.cat.pk,
                "technologies_ids": [self.tech.pk],
                "competences_ids": [self.comp.pk],
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        article = Article.objects.get(slug="nouvel-article")
        self.assertEqual(article.technologies.count(), 1)
        self.assertEqual(article.competences.count(), 1)

class ArticleWorkflowAPITest(TestCase):
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
        self.cat = Categorie.objects.create(
            nom="Test Workflow", type=Categorie.TypeChoices.ARTICLE
        )
        self.article = Article.objects.create(
            titre="Workflow Test",
            categorie=self.cat,
            auteur=self.admin,
            statut=Article.StatutChoices.BROUILLON,
        )

    def _url(self, action: str) -> str:
        return f"/api/articles/articles/{self.article.slug}/{action}/"

    def test_soumettre_refuse_anonyme(self):
        response = self.client.post(self._url("soumettre"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_soumettre_autorise_editeur(self):
        self.client.force_authenticate(user=self.editeur)
        response = self.client.post(self._url("soumettre"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.article.refresh_from_db()
        self.assertEqual(self.article.statut, Article.StatutChoices.EN_REVISION)

    def test_soumettre_refuse_si_deja_en_revision(self):
        self.article.statut = Article.StatutChoices.EN_REVISION
        self.article.save()
        self.client.force_authenticate(user=self.editeur)
        response = self.client.post(self._url("soumettre"))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valider_refuse_editeur(self):
        self.article.statut = Article.StatutChoices.EN_REVISION
        self.article.save()
        self.client.force_authenticate(user=self.editeur)
        response = self.client.post(self._url("valider"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_valider_autorise_admin(self):
        self.article.statut = Article.StatutChoices.EN_REVISION
        self.article.save()
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self._url("valider"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.article.refresh_from_db()
        self.assertEqual(self.article.statut, Article.StatutChoices.VALIDE)

    def test_publier_autorise_admin_depuis_brouillon(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self._url("publier"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.article.refresh_from_db()
        self.assertEqual(self.article.statut, Article.StatutChoices.PUBLIE)

    def test_publier_refuse_editeur(self):
        self.client.force_authenticate(user=self.editeur)
        response = self.client.post(self._url("publier"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_depublier_autorise_admin(self):
        self.article.statut = Article.StatutChoices.PUBLIE
        self.article.save()
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self._url("depublier"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.article.refresh_from_db()
        self.assertEqual(self.article.statut, Article.StatutChoices.BROUILLON)

    def test_depublier_refuse_si_pas_publie(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self._url("depublier"))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_archiver_autorise_admin_depuis_publie(self):
        self.article.statut = Article.StatutChoices.PUBLIE
        self.article.save()
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self._url("archiver"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.article.refresh_from_db()
        self.assertEqual(self.article.statut, Article.StatutChoices.ARCHIVE)

    def test_archiver_refuse_depuis_brouillon(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self._url("archiver"))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)