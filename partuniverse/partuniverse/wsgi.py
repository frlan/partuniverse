import os
from django.core.wsgi import get_wsgi_application


"""
WSGI config for partuniverse project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "partuniverse.settings")

application = get_wsgi_application()
