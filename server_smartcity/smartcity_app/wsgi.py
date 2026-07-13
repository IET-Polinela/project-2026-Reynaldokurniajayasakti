"""
WSGI config for smartcity_app project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Perubahan dari 'iet_24782061_2026.settings' menjadi 'smartcity_app.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartcity_app.settings')

application = get_wsgi_application()