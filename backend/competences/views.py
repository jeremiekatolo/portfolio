"""
ViewSets DRF pour l'app competences.

Permissions :
- Lecture publique.
- Écriture réservée aux rôles editeur et administrateur (ou superuser).
"""

from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import BasePermission

from .models import Competence
from .serializers import CompetenceSerializer

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


class CompetenceViewSet(viewsets.ModelViewSet):
    """CRUD sur les compétences."""

    queryset = Competence.objects.all()
    serializer_class = CompetenceSerializer
    permission_classes = [PeutEditerContenu]
    filterset_fields = ["domaine"]
    search_fields = ["nom", "description"]
    ordering_fields = ["domaine", "ordre", "nom"]