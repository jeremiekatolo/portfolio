"""
ViewSets DRF pour l'app articles.
"""

from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import BasePermission

from .models import Article
from .serializers import ArticleEcritureSerializer, ArticleSerializer

Utilisateur = get_user_model()


class PeutEditerContenu(BasePermission):
    """Écriture : editeur, administrateur ou superuser."""

    def has_permission(self, request, view):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        return user.role in (Utilisateur.Role.EDITEUR, Utilisateur.Role.ADMINISTRATEUR)


class ArticleViewSet(viewsets.ModelViewSet):
    """CRUD sur les articles."""

    permission_classes = [PeutEditerContenu]
    lookup_field = "slug"
    filterset_fields = ["categorie", "statut"]
    search_fields = ["titre", "resume", "contenu"]
    ordering_fields = ["ordre", "date_creation", "temps_lecture"]

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