"""
WSGI config for shakespeare project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os, sys
sys.path.insert(0, '/opt/python/current/app') #Thanks http://stackoverflow.com/a/26822650/7322725

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shakespeare.settings.production")


application = get_wsgi_application()
