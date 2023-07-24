"""
WSGI config for project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from dotenv import load_dotenv
load_dotenv()

if os.environ.get("DEBUG") == 1 and os.environ.get("PRODUCTION") == 0:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.conf.dev')

elif os.environ.get("DEBUG") == 0 and os.environ.get("PRODUCTION") == 0:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.conf.stage')

else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.conf.prod')
print(os.environ.get('DEBUG') == 1, os.environ.get('PRODUCTION') == 0)

application = get_wsgi_application()
