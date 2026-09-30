"""
Mixins DRF transverses.

PublicationActionsMixin : ajoute les actions `soumettre`, `valider`,
`publier`, `depublier`, `archiver` à un ViewSet.

Le ViewSet concret doit :
- définir `service_module` (ex. : projets.services)
- exposer `get_serializer_class()` (déjà fait partout)

Le module de service doit exposer les fonctions :
- soumettre(instance, user, request) -> instance
- valider(instance, user, request) -> instance
- publier(instance, user, request) -> instance
- depublier(instance, user, request) -> instance
- archiver(instance, user, request) -> instance

Chaque fonction lève `TransitionInvalide` ou `ActionNonAutorisee` en cas
d'erreur, ce que le mixin transforme en réponse 400.
"""

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from .exceptions import ActionNonAutorisee, TransitionInvalide
from .permissions import EstAdminSeul, EstEditeurOuAdmin


class PublicationActionsMixin:
    """
    Ajoute 5 actions POST de workflow de publication.

    Les actions retournent l'objet complet mis à jour (200) ou une erreur (400).
    """

    # À surcharger dans chaque ViewSet concret.
    service_module = None

    def _executer_action(self, request, nom_action: str):
        """Méthode interne : exécute une action de service et formate la réponse."""
        if self.service_module is None:
            return Response(
                {"detail": "Aucun module de service configuré."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        fonction = getattr(self.service_module, nom_action, None)
        if fonction is None:
            return Response(
                {"detail": f"Action `{nom_action}` non implémentée."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        instance = self.get_object()
        try:
            instance = fonction(instance, user=request.user, request=request)
        except TransitionInvalide as exc:
            return Response(
                {"detail": exc.message}, status=status.HTTP_400_BAD_REQUEST
            )
        except ActionNonAutorisee as exc:
            return Response(
                {"detail": exc.message}, status=status.HTTP_403_FORBIDDEN
            )

        # On utilise le serializer de lecture pour renvoyer l'objet complet.
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], permission_classes=[EstEditeurOuAdmin])
    def soumettre(self, request, *args, **kwargs):
        """Brouillon → En révision. Accessible aux éditeurs."""
        return self._executer_action(request, "soumettre")

    @action(detail=True, methods=["post"], permission_classes=[EstAdminSeul])
    def valider(self, request, *args, **kwargs):
        """En révision → Validé. Réservé aux administrateurs."""
        return self._executer_action(request, "valider")

    @action(detail=True, methods=["post"], permission_classes=[EstAdminSeul])
    def publier(self, request, *args, **kwargs):
        """Brouillon / En révision / Validé → Publié. Réservé aux administrateurs."""
        return self._executer_action(request, "publier")

    @action(detail=True, methods=["post"], permission_classes=[EstAdminSeul])
    def depublier(self, request, *args, **kwargs):
        """Publié → Brouillon. Réservé aux administrateurs."""
        return self._executer_action(request, "depublier")

    @action(detail=True, methods=["post"], permission_classes=[EstAdminSeul])
    def archiver(self, request, *args, **kwargs):
        """Validé / Publié → Archivé. Réservé aux administrateurs."""
        return self._executer_action(request, "archiver")