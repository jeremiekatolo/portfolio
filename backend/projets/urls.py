"""
URLs de l'app projets.

Montées sous /api/projets/ depuis configuration/urls.py.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ProjetViewSet

app_name = "projets"

router = DefaultRouter()
router.register(r"projets", ProjetViewSet, basename="projet")

urlpatterns = [
    path("", include(router.urls)),
]