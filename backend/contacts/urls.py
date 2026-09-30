"""
URLs de l'app contacts.

Montées sous /api/contacts/ depuis configuration/urls.py.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ContactViewSet

app_name = "contacts"

router = DefaultRouter()
router.register(r"contacts", ContactViewSet, basename="contact")

urlpatterns = [
    path("", include(router.urls)),
]