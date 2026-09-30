"""
ViewSets DRF pour l'app projets.

Workflow de publication exposé via PublicationActionsMixin :
- POST /api/projets/projets/<slug>/soumettre/
- POST /api/projets/projets/<slug>/valider/
- POST /api/projets/projets/<slug>/publier/
- POST /api/projets/projets/<slug>/depublier/
- POST /api/projets/projets/<slug>/archiver/

Règle de visibilité publique :
- Un Projet avec statut != `publie` n'est PAS accessible publiquement,
  même en connaissant son slug.
- Les éditeurs et administrateurs voient tous les projets.
"""

from django.contrib.auth import get_user_model
from rest_framework import viewsets

from core.mixins import PublicationActionsMixin
from core.permissions import EstEditeurOuAdmin

from . import services
from .models import Projet
from .serializers import ProjetEcritureSerializer, ProjetSerializer

Utilisateur = get_user_model()


class ProjetViewSet(PublicationActionsMixin, viewsets.ModelViewSet):
    """
    CRUD + workflow de publication sur les projets.

    - Lecture : seuls les projets publics sont visibles pour un visiteur.
    - Écriture : éditeurs et administrateurs.
    - Actions workflow : voir PublicationActionsMixin.
    """

    permission_classes = [EstEditeurOuAdmin]
    lookup_field = "slug"
    filterset_fields = ["categorie", "difficulte", "statut", "mis_en_avant"]
    search_fields = ["titre", "resume", "description", "probleme", "contexte"]
    ordering_fields = ["date_realisation", "ordre", "date_creation"]

    # Config du mixin : indique où trouver les fonctions de transition.
    service_module = services

    def get_queryset(self):
        """Filtre les projets selon le rôle de l'utilisateur."""
        user = self.request.user
        if user.is_authenticated and (
            user.is_superuser
            or user.role
            in (Utilisateur.Role.EDITEUR, Utilisateur.Role.ADMINISTRATEUR)
        ):
            return (
                Projet.objects.select_related(
                    "categorie", "laboratoire", "etude_de_cas", "auteur", "seo_image"
                )
                .prefetch_related("technologies", "competences")
                .all()
            )
        return (
            Projet.objects.publies()
            .select_related(
                "categorie", "laboratoire", "etude_de_cas", "auteur", "seo_image"
            )
            .prefetch_related("technologies", "competences")
        )

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return ProjetEcritureSerializer
        return ProjetSerializer