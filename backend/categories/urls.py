"""
URLs de l'app categories.

Montées sous /api/categories/ depuis configuration/urls.py.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategorieViewSet

app_name = "categories"

router = DefaultRouter()
router.register(r"categories", CategorieViewSet, basename="categorie")

urlpatterns = [
    path("", include(router.urls)),
]