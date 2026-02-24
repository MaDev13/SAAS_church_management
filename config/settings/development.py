"""
Development settings - debug mode, local DB, verbose logging.
"""
from .base import *  # noqa: F401, F403

DEBUG = True

# Use SQLite for dev if PostgreSQL not configured (optional)
import os
if os.environ.get("USE_SQLITE"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "db.sqlite3",
        }
    }
ALLOWED_HOSTS = ["*"]

# LocMem for dev if Redis unavailable
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

CORS_ALLOW_ALL_ORIGINS = True
