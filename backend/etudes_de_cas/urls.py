"""
URLs de l'app etudes_de_cas.

Montées sous /api/etudes-de-cas/ depuis configuration/urls.py.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import EtudeDeCasViewSet

app_name = "etudes_de_cas"

router = DefaultRouter()
router.register(r"etudes-de-cas", EtudeDeCasViewSet, basename="etudedecas")

urlpatterns = [
    path("", include(router.urls)),
]