"""
URLconf racine du projet.

- /admin/ : administration Django.
- /api/utilisateurs/ : API de l'app utilisateurs (ViewSets + /moi/).
- /api/ : à compléter app par app au fur et à mesure.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/utilisateurs/",
        include("utilisateurs.urls", namespace="utilisateurs"),
    ),
]

# En développement uniquement : servir les médias et les fichiers statiques.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)