from django.urls import path
from .views import chat

urlpatterns = [
    path('<str:room_name>', chat, name='chat'),
]