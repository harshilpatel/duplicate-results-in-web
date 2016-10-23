"""
WSGI config for beproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "beproject.settings")

application = get_wsgi_application()

if os.environ.get('heroku'):
	from dj_static import Cling
	application = Cling(get_wsgi_application())