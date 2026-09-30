"""
ViewSets DRF pour l'app contacts.

Permissions différenciées :
- POST (créer) : public (allow_any).
- GET liste / détail : admin uniquement.
- PATCH / DELETE : admin uniquement.
"""

from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import Contact
from .serializers import ContactAdminSerializer, ContactPublicSerializer

Utilisateur = get_user_model()


class PermissionContact(BasePermission):
    """
    Règles :
    - POST : tout le monde (formulaire public).
    - GET / PATCH / DELETE : admin uniquement.
    """

    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        return user.role == Utilisateur.Role.ADMINISTRATEUR


class ContactViewSet(viewsets.ModelViewSet):
    """CRUD sur les messages de contact."""

    queryset = Contact.objects.all()
    permission_classes = [PermissionContact]
    filterset_fields = ["statut"]
    search_fields = ["nom", "email", "sujet", "message"]
    ordering_fields = ["date_envoi"]
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_serializer_class(self):
        if self.action == "create":
            return ContactPublicSerializer
        return ContactAdminSerializer

    def perform_create(self, serializer):
        """Renseigne ip_hash et user_agent depuis la requête."""
        ip = self._get_client_ip(self.request)
        ua = self.request.META.get("HTTP_USER_AGENT", "")[:300]
        serializer.save(
            ip_hash=Contact.hasher_ip(ip),
            user_agent=ua,
        )

    @staticmethod
    def _get_client_ip(request) -> str:
        """Récupère l'IP client, en tenant compte d'un éventuel proxy."""
        xff = request.META.get("HTTP_X_FORWARDED_FOR", "")
        if xff:
            return xff.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR", "")