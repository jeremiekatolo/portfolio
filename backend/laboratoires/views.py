"""
ViewSets DRF pour l'app laboratoires.
"""

from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import BasePermission

from .models import Laboratoire
from .serializers import LaboratoireEcritureSerializer, LaboratoireSerializer

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


class LaboratoireViewSet(viewsets.ModelViewSet):
    """CRUD sur les laboratoires."""

    permission_classes = [PeutEditerContenu]
    lookup_field = "slug"
    filterset_fields = ["difficulte", "statut"]
    search_fields = ["titre", "objectif", "problematique", "environnement"]
    ordering_fields = ["ordre", "date_creation", "difficulte"]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and (
            user.is_superuser
            or user.role
            in (Utilisateur.Role.EDITEUR, Utilisateur.Role.ADMINISTRATEUR)
        ):
            return (
                Laboratoire.objects.select_related("auteur", "seo_image")
                .prefetch_related("technologies", "competences")
                .all()
            )
        return (
            Laboratoire.objects.publies()
            .select_related("auteur", "seo_image")
            .prefetch_related("technologies", "competences")
        )

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return LaboratoireEcritureSerializer
        return LaboratoireSerializer