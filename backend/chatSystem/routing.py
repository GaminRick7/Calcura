"""
File: routing.py
Authors: Raihaan Sandhu and Darun Kanesalingam
Last Modified: April 27, 2023
Version: 1.0.0

This file handles websocket routing to the URL ChatConsumer.
"""

from django.urls import path, re_path
from chatSystem.consumers import ChatConsumer
 
# Here, "" is routing to the URL ChatConsumer which
# will handle the chat functionality.

#Code adapted from [5], used to create the websocket routings
websocket_urlpatterns = [
    #Websocket routing to host multiple different chat rooms
    re_path(r'ws/chat/(?P<roomId>\w+)/$' , ChatConsumer.as_asgi()),
]