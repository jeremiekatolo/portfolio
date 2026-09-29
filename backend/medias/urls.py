"""
URLs de l'app medias.

Montées sous /api/medias/ depuis configuration/urls.py.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import LienExterneViewSet, MediaLienViewSet, MediaViewSet

app_name = "medias"

router = DefaultRouter()
router.register(r"medias", MediaViewSet, basename="media")
router.register(r"liens", MediaLienViewSet, basename="medialien")
router.register(r"liens-externes", LienExterneViewSet, basename="lienexterne")

urlpatterns = [
    path("", include(router.urls)),
]