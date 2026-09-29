"""
ViewSets DRF pour l'app medias.

- MediaViewSet      : upload et gestion des fichiers.
- MediaLienViewSet  : liaisons média ↔ contenu.
- LienExterneViewSet: liens externes polymorphes.

Permissions :
- Lecture publique.
- Écriture réservée aux rôles editeur et administrateur (ou superuser).
"""

from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import BasePermission

from .models import LienExterne, Media, MediaLien
from .serializers import LienExterneSerializer, MediaLienSerializer, MediaSerializer

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


class MediaViewSet(viewsets.ModelViewSet):
    """CRUD sur les médias (avec upload multipart)."""

    queryset = Media.objects.select_related("uploaded_by").all()
    serializer_class = MediaSerializer
    permission_classes = [PeutEditerContenu]
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    filterset_fields = ["type", "est_orphelin"]
    search_fields = ["nom_original", "alt_text", "hash_sha256"]
    ordering_fields = ["uploaded_at", "taille", "nom_original"]


class MediaLienViewSet(viewsets.ModelViewSet):
    """CRUD sur les liaisons média ↔ contenu."""

    queryset = MediaLien.objects.select_related("media", "content_type").all()
    serializer_class = MediaLienSerializer
    permission_classes = [PeutEditerContenu]
    filterset_fields = ["role", "content_type", "object_id"]
    ordering_fields = ["ordre", "id"]


class LienExterneViewSet(viewsets.ModelViewSet):
    """CRUD sur les liens externes polymorphes."""

    queryset = LienExterne.objects.select_related("content_type").all()
    serializer_class = LienExterneSerializer
    permission_classes = [PeutEditerContenu]
    filterset_fields = ["type", "content_type", "object_id"]
    ordering_fields = ["ordre", "id"]