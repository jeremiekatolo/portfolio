"""
ViewSets DRF pour l'app etudes_de_cas.

Workflow de publication exposé via PublicationActionsMixin.
"""

from django.contrib.auth import get_user_model
from rest_framework import viewsets

from core.mixins import PublicationActionsMixin
from core.permissions import EstEditeurOuAdmin

from . import services
from .models import EtudeDeCas
from .serializers import EtudeDeCasEcritureSerializer, EtudeDeCasSerializer

Utilisateur = get_user_model()


class EtudeDeCasViewSet(PublicationActionsMixin, viewsets.ModelViewSet):
    """CRUD + workflow de publication sur les études de cas."""

    permission_classes = [EstEditeurOuAdmin]
    lookup_field = "slug"
    filterset_fields = ["statut"]
    search_fields = ["titre", "probleme", "contexte", "analyse"]
    ordering_fields = ["ordre", "date_creation"]

    service_module = services

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