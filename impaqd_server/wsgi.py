"""
WSGI config for impaqd_server project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/

By default, uses the production settings, since this is typically the
configuration using this file.
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "impaqd_server.settings.production")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

