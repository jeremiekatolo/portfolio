"""
Configuration de développement.

Règles :
- DEBUG = True
- Hôtes permissifs
- Jamais utilisé en production
"""

from .base import *  # noqa: F401,F403

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

# En dev : HTTP autorisé
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False