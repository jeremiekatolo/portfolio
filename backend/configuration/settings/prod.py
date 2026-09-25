"""
Configuration de production.

Règles :
- DEBUG = False
- HTTPS obligatoire
- HSTS activé
- Cookies sécurisés
- Aucune information sensible dans les erreurs
"""

from .base import *  # noqa: F401,F403

DEBUG = False

# À ajuster au moment du déploiement
ALLOWED_HOSTS: list[str] = []

# --- HTTPS ---
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = 31536000  # 1 an
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# --- Cookies ---
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True