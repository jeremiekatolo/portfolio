"""
URLs de l'app technologies.

Montées sous /api/technologies/ depuis configuration/urls.py.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TechnologieViewSet

app_name = "technologies"

router = DefaultRouter()
router.register(r"technologies", TechnologieViewSet, basename="technologie")

urlpatterns = [
    path("", include(router.urls)),
]