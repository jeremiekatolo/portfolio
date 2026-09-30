"""
ViewSets DRF pour l'app etudes_de_cas.
"""

from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import BasePermission

from .models import EtudeDeCas
from .serializers import EtudeDeCasEcritureSerializer, EtudeDeCasSerializer

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


class EtudeDeCasViewSet(viewsets.ModelViewSet):
    """CRUD sur les études de cas."""

    permission_classes = [PeutEditerContenu]
    lookup_field = "slug"
    filterset_fields = ["statut"]
    search_fields = ["titre", "probleme", "contexte", "analyse"]
    ordering_fields = ["ordre", "date_creation"]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and (
            user.is_superuser
            or user.role
            in (Utilisateur.Role.EDITEUR, Utilisateur.Role.ADMINISTRATEUR)
        ):
            return (
                EtudeDeCas.objects.select_related("auteur", "seo_image")
                .prefetch_related("technologies", "competences")
                .all()
            )
        return (
            EtudeDeCas.objects.publies()
            .select_related("auteur", "seo_image")
            .prefetch_related("technologies", "competences")
        )

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return EtudeDeCasEcritureSerializer
        return EtudeDeCasSerializer