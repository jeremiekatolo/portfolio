"""
ViewSets DRF pour l'app utilisateurs.

- UtilisateurViewSet : CRUD Utilisateur (réservé aux admins pour l'écriture).
- ProfilViewSet      : CRUD Profil.
- MeView             : vue « moi » (utilisateur connecté uniquement).

Permissions :
- Lecture : tout le monde (IsAuthenticatedOrReadOnly global).
- Écriture : utilisateurs authentifiés avec rôle editeur ou administrateur
  (permission custom ci-dessous).
"""

from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Profil
from .serializers import MeSerializer, ProfilSerializer, UtilisateurSerializer

Utilisateur = get_user_model()


class PeutEditerContenu(BasePermission):
    """
    Autorise l'écriture uniquement aux rôles editeur ou administrateur,
    ou aux superusers Django.
    """

    def has_permission(self, request, view):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        return user.role in (Utilisateur.Role.EDITEUR, Utilisateur.Role.ADMINISTRATEUR)


class UtilisateurViewSet(viewsets.ModelViewSet):
    """CRUD sur les utilisateurs."""

    queryset = Utilisateur.objects.all().order_by("username")
    serializer_class = UtilisateurSerializer
    permission_classes = [PeutEditerContenu]
    filterset_fields = ["role", "is_active"]
    search_fields = ["username", "email", "first_name", "last_name"]
    ordering_fields = ["username", "date_joined"]


class ProfilViewSet(viewsets.ModelViewSet):
    """CRUD sur les profils."""

    queryset = Profil.objects.select_related(
        "utilisateur", "photo", "cv", "seo_image_defaut"
    ).all()
    serializer_class = ProfilSerializer
    permission_classes = [PeutEditerContenu]
    filterset_fields = ["disponible"]
    search_fields = ["nom_public", "titre_principal", "utilisateur__username"]
    ordering_fields = ["date_modification"]


class MeView(APIView):
    """Retourne l'utilisateur connecté avec son profil imbriqué."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = MeSerializer(request.user)
        return Response(serializer.data)