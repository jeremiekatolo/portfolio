"""
URLs de l'app parcours.

Montées sous /api/parcours/ depuis configuration/urls.py.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CertificationViewSet, ParcoursViewSet

app_name = "parcours"

router = DefaultRouter()
router.register(r"parcours", ParcoursViewSet, basename="parcours")
router.register(r"certifications", CertificationViewSet, basename="certification")

urlpatterns = [
    path("", include(router.urls)),
]