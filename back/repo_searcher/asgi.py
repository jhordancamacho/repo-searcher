"""
ASGI config for repo_searcher project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from pathlib import Path
from django.core.asgi import get_asgi_application
import environ

env = environ.Env(DEBUG=(bool, True))
BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
SETT_ENV = env("SETTINGS_ENVIRONMENT")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", SETT_ENV)

application = get_asgi_application()
