"""WSGI config for the DevBoard project."""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devboard.settings')

application = get_wsgi_application()
