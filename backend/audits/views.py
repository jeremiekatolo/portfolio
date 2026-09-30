"""
Views pour l'app audits.

Lecture seule, admin uniquement.
"""

from rest_framework import viewsets
from rest_framework.permissions import BasePermission

from .models import AuditLog
from .serializers import AuditLogSerializer
from django.contrib.auth import get_user_model

Utilisateur = get_user_model()


class EstAdministrateur(BasePermission):
    """Accès réservé aux administrateurs (ou superusers)."""

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        return user.role == Utilisateur.Role.ADMINISTRATEUR


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """Consultation du journal d'audit (lecture seule, admin)."""

    queryset = AuditLog.objects.select_related(
        "utilisateur", "content_type"
    ).all()
    serializer_class = AuditLogSerializer
    permission_classes = [EstAdministrateur]
    filterset_fields = ["action", "resultat", "utilisateur", "content_type"]
    search_fields = ["metadonnees"]
    ordering_fields = ["date"]