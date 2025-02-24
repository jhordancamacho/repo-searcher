"""
WSGI config for repo_searcher project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from pathlib import Path
from django.core.wsgi import get_wsgi_application
import environ

env = environ.Env(DEBUG=(bool, True))
BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
SETT_ENV = env("SETTINGS_ENVIRONMENT")


os.environ.setdefault("DJANGO_SETTINGS_MODULE", SETT_ENV)

application = get_wsgi_application()
