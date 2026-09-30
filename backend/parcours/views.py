"""
ViewSets DRF pour l'app parcours.
"""

from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import BasePermission

from .models import Certification, Parcours
from .serializers import (
    CertificationEcritureSerializer,
    CertificationSerializer,
    ParcoursEcritureSerializer,
    ParcoursSerializer,
)

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


class ParcoursViewSet(viewsets.ModelViewSet):
    """CRUD sur les entrées de parcours."""

    queryset = Parcours.objects.select_related("profil").prefetch_related("competences").all()
    permission_classes = [PeutEditerContenu]
    filterset_fields = ["type", "profil"]
    search_fields = ["titre", "organisation", "description"]
    ordering_fields = ["date_debut", "date_fin", "ordre"]

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return ParcoursEcritureSerializer
        return ParcoursSerializer


class CertificationViewSet(viewsets.ModelViewSet):
    """CRUD sur les certifications."""

    queryset = (
        Certification.objects.select_related("profil", "badge")
        .prefetch_related("competences")
        .all()
    )
    permission_classes = [PeutEditerContenu]
    filterset_fields = ["profil"]
    search_fields = ["nom", "organisme", "description"]
    ordering_fields = ["date_obtention", "date_expiration", "ordre"]

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return CertificationEcritureSerializer
        return CertificationSerializer