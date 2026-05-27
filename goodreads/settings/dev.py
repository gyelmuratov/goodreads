from decouple import config

from .base import *  # noqa: F403,F401


DEBUG = config("DJANGO_DEBUG", default=True, cast=bool)
ALLOWED_HOSTS = ["*"]

