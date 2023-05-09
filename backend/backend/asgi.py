import os
from django.core.asgi import get_asgi_application
import time
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ChatApp.settings')
 
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter , URLRouter
from chatSystem import routing
 
application = ProtocolTypeRouter(
    {
        "http" : get_asgi_application() ,
        "websocket" : AuthMiddlewareStack(
            URLRouter(
                routing.websocket_urlpatterns
            )   
        )
    }
)
