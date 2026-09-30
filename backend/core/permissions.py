"""
Permissions DRF réutilisables.

Centralise les permissions utilisées dans toutes les apps pour éviter
la duplication (auparavant : PeutEditerContenu dans 8 fichiers).

Convention :
- Lecture (GET/HEAD/OPTIONS) : publique par défaut.
- Écriture : éditeur + administrateur + superuser.

Note : `get_user_model()` est appelé à l'intérieur des méthodes, jamais
au niveau du module, pour éviter des erreurs d'import avant que Django
soit complètement chargé.
"""

from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission, SAFE_METHODS


class EstEditeurOuAdmin(BasePermission):
    """
    Autorise la lecture à tous.

    Autorise l'écriture (POST, PUT, PATCH, DELETE) aux :
    - superusers Django
    - utilisateurs avec rôle `editeur`
    - utilisateurs avec rôle `administrateur`
    """

    message = "Vous devez être éditeur ou administrateur pour effectuer cette action."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        Utilisateur = get_user_model()
        return user.role in (Utilisateur.Role.EDITEUR, Utilisateur.Role.ADMINISTRATEUR)


class EstAdminSeul(BasePermission):
    """
    Autorise l'accès aux administrateurs uniquement.

    Utilisé pour les actions sensibles :
    - valider, publier, dépublier, archiver un contenu
    - consulter le journal d'audit
    - modifier les contacts
    """

    message = "Cette action est réservée aux administrateurs."

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        Utilisateur = get_user_model()
        return user.role == Utilisateur.Role.ADMINISTRATEUR