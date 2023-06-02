"""
File: asgi.py
Authors: Raihaan Sandhu and Darun Kanesalingam
Last Modified: May 15, 2023
Version: 1.0.0

This file contains the configurations for the ASGI (Asynchronous Server Gateway Interface)
"""

import os
from django.core.asgi import get_asgi_application
import time
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ChatApp.settings')
 
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter , URLRouter
from chatSystem import routing

#Code adapted from [5], used to create the asgi application to host channels and all chatsystem specific actions
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
