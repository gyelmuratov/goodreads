from decouple import config

from .base import *  # noqa: F403,F401


DEBUG = False
ALLOWED_HOSTS = [host.strip() for host in config("ALLOWED_HOSTS").split(",") if host.strip()]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

