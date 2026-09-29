"""
URLs de l'app competences.

Montées sous /api/competences/ depuis configuration/urls.py.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CompetenceViewSet

app_name = "competences"

router = DefaultRouter()
router.register(r"competences", CompetenceViewSet, basename="competence")

urlpatterns = [
    path("", include(router.urls)),
]