"""
Exceptions métier transverses.

Utilisées par les services (services.py) pour signaler une erreur métier
que le mixin DRF transformera en réponse HTTP 400.
"""


class TransitionInvalide(Exception):
    """
    Levée lorsqu'une transition de statut est invalide.

    Exemple : tenter de publier un contenu déjà archivé.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class ActionNonAutorisee(Exception):
    """
    Levée lorsqu'un utilisateur tente une action interdite par son rôle.

    Exemple : un éditeur tente de publier.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)