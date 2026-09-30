"""
ViewSets DRF pour l'app laboratoires.

Workflow de publication exposé via PublicationActionsMixin.
"""

from django.contrib.auth import get_user_model
from rest_framework import viewsets

from core.mixins import PublicationActionsMixin
from core.permissions import EstEditeurOuAdmin

from . import services
from .models import Laboratoire
from .serializers import LaboratoireEcritureSerializer, LaboratoireSerializer

Utilisateur = get_user_model()


class LaboratoireViewSet(PublicationActionsMixin, viewsets.ModelViewSet):
    """CRUD + workflow de publication sur les laboratoires."""

    permission_classes = [EstEditeurOuAdmin]
    lookup_field = "slug"
    filterset_fields = ["difficulte", "statut"]
    search_fields = ["titre", "objectif", "problematique", "environnement"]
    ordering_fields = ["ordre", "date_creation", "difficulte"]

    service_module = services

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