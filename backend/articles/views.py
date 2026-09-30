"""
ViewSets DRF pour l'app articles.

Workflow de publication exposé via PublicationActionsMixin.
"""

from django.contrib.auth import get_user_model
from rest_framework import viewsets

from core.mixins import PublicationActionsMixin
from core.permissions import EstEditeurOuAdmin

from . import services
from .models import Article
from .serializers import ArticleEcritureSerializer, ArticleSerializer

Utilisateur = get_user_model()


class ArticleViewSet(PublicationActionsMixin, viewsets.ModelViewSet):
    """CRUD + workflow de publication sur les articles."""

    permission_classes = [EstEditeurOuAdmin]
    lookup_field = "slug"
    filterset_fields = ["categorie", "statut"]
    search_fields = ["titre", "resume", "contenu"]
    ordering_fields = ["ordre", "date_creation", "temps_lecture"]

    service_module = services

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and (
            user.is_superuser
            or user.role
            in (Utilisateur.Role.EDITEUR, Utilisateur.Role.ADMINISTRATEUR)
        ):
            return (
                Article.objects.select_related(
                    "categorie", "auteur", "seo_image"
                )
                .prefetch_related("technologies", "competences")
                .all()
            )
        return (
            Article.objects.publies()
            .select_related("categorie", "auteur", "seo_image")
            .prefetch_related("technologies", "competences")
        )

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return ArticleEcritureSerializer
        return ArticleSerializer