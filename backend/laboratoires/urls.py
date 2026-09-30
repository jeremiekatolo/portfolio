"""
URLs de l'app laboratoires.

Montées sous /api/laboratoires/ depuis configuration/urls.py.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import LaboratoireViewSet

app_name = "laboratoires"

router = DefaultRouter()
router.register(r"laboratoires", LaboratoireViewSet, basename="laboratoire")

urlpatterns = [
    path("", include(router.urls)),
]