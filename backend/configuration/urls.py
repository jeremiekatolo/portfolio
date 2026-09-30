"""
URLconf racine du projet.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/utilisateurs/", include("utilisateurs.urls", namespace="utilisateurs")),
    path("api/medias/", include("medias.urls", namespace="medias")),
    path("api/categories/", include("categories.urls", namespace="categories")),
    path("api/technologies/", include("technologies.urls", namespace="technologies")),
    path("api/competences/", include("competences.urls", namespace="competences")),
    path("api/projets/", include("projets.urls", namespace="projets")),
    path("api/laboratoires/", include("laboratoires.urls", namespace="laboratoires")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)