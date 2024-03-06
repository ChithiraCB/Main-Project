"""
WSGI config for fashion project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_asgi_application
from channels.routing import ProtocolTypeRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fashion.settings')

#application = get_wsgi_application()

application=ProtocolTypeRouter({
    'http':get_asgi_application

})
