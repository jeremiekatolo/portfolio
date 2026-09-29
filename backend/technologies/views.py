"""
ViewSets DRF pour l'app technologies.

Permissions :
- Lecture publique.
- Écriture réservée aux rôles editeur et administrateur (ou superuser).
"""

from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import BasePermission

from .models import Technologie
from .serializers import TechnologieSerializer

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


class TechnologieViewSet(viewsets.ModelViewSet):
    """CRUD sur les technologies."""

    queryset = Technologie.objects.select_related("logo").all()
    serializer_class = TechnologieSerializer
    permission_classes = [PeutEditerContenu]
    filterset_fields = ["categorie_tech"]
    search_fields = ["nom", "description"]
    ordering_fields = ["categorie_tech", "ordre", "nom"]