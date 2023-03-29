from django.urls import path, re_path
from chatSystem.consumers import ChatConsumer
 
# Here, "" is routing to the URL ChatConsumer which
# will handle the chat functionality.
print("HI")
websocket_urlpatterns = [
    #Websocket routing to host multiple different chat rooms
    re_path(r'ws/chat/(?P<roomId>\w+)/$' , ChatConsumer.as_asgi()),
]