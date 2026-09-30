"""
URLs de l'app audits.

Montées sous /api/audits/ depuis configuration/urls.py.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AuditLogViewSet

app_name = "audits"

router = DefaultRouter()
router.register(r"logs", AuditLogViewSet, basename="auditlog")

urlpatterns = [
    path("", include(router.urls)),
]