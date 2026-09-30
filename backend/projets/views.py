"""
ViewSets DRF pour l'app projets.

Règle de visibilité publique :
- Un Projet avec statut != `publie` n'est PAS accessible publiquement,
  même en connaissant son slug ou son id.
- Les éditeurs et administrateurs voient tous les projets.
"""

from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import BasePermission

from .models import Projet
from .serializers import ProjetEcritureSerializer, ProjetSerializer

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


class ProjetViewSet(viewsets.ModelViewSet):
    """
    CRUD sur les projets.

    - Lecture : seuls les projets publics sont visibles pour un visiteur.
    - Écriture : éditeurs et administrateurs.
    """

    permission_classes = [PeutEditerContenu]
    lookup_field = "slug"
    filterset_fields = ["categorie", "difficulte", "statut", "mis_en_avant"]
    search_fields = ["titre", "resume", "description", "probleme", "contexte"]
    ordering_fields = ["date_realisation", "ordre", "date_creation"]

    def get_queryset(self):
        """Filtre les projets selon le rôle de l'utilisateur."""
        user = self.request.user
        if user.is_authenticated and (
            user.is_superuser
            or user.role
            in (Utilisateur.Role.EDITEUR, Utilisateur.Role.ADMINISTRATEUR)
        ):
            return (
                Projet.objects.select_related(
                    "categorie", "laboratoire", "etude_de_cas", "auteur", "seo_image"
                )
                .prefetch_related("technologies", "competences")
                .all()
            )
        return (
            Projet.objects.publies()
            .select_related(
                "categorie", "laboratoire", "etude_de_cas", "auteur", "seo_image"
            )
            .prefetch_related("technologies", "competences")
        )

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return ProjetEcritureSerializer
        return ProjetSerializer