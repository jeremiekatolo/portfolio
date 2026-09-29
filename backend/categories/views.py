"""
ViewSets DRF pour l'app categories.

Permissions :
- Lecture publique.
- Écriture réservée aux rôles editeur et administrateur (ou superuser).
"""

from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import BasePermission

from .models import Categorie
from .serializers import CategorieSerializer

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


class CategorieViewSet(viewsets.ModelViewSet):
    """CRUD sur les catégories."""

    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = [PeutEditerContenu]
    filterset_fields = ["type"]
    search_fields = ["nom", "slug", "description"]
    ordering_fields = ["type", "ordre", "nom"]