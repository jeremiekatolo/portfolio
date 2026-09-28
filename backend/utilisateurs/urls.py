"""
URLs de l'app utilisateurs.

Montées sous /api/utilisateurs/ depuis configuration/urls.py.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import MeView, ProfilViewSet, UtilisateurViewSet

app_name = "utilisateurs"

router = DefaultRouter()
router.register(r"utilisateurs", UtilisateurViewSet, basename="utilisateur")
router.register(r"profils", ProfilViewSet, basename="profil")

urlpatterns = [
    path("moi/", MeView.as_view(), name="me"),
    path("", include(router.urls)),
]