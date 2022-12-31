"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack #auth middleware import
from channels.routing import ProtocolTypeRouter, URLRouter #second import needed
import chatapp.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

#With websockets:
application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket':AuthMiddlewareStack(
        URLRouter(
            chatapp.routing.websocket_urlpatterns
        )
    ),
    
}) #setting HTTP protocol and websocket, so app could use both


# BEFORE:application = get_asgi_application()


#modifications to work with web sockets:
#imports
#connect routing.py
#websocket_urlpatters are the ones defined in routing.py