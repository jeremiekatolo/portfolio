"""
URLconf racine du projet.

- /admin/ : administration Django.
- /api/utilisateurs/ : API utilisateurs.
- /api/medias/ : API medias.
- /api/categories/ : API categories.
- /api/technologies/ : API technologies.
- /api/ : à compléter app par app.
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
    path(
        "api/medias/",
        include("medias.urls", namespace="medias"),
    ),
    path(
        "api/categories/",
        include("categories.urls", namespace="categories"),
    ),
    path(
        "api/technologies/",
        include("technologies.urls", namespace="technologies"),
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)