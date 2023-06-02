"""
File: urls.py
Authors: Raihaan Sandhu and Darun Kanesalingam
Last Modified: April 13, 2023
Version: 1.0.0

This file contains the URL routing for the chatSystem.
"""

from django.urls import path, include
from chatSystem import views 
 
urlpatterns = [
    #Urlpaths for chat rooms and generic chat page
    path("<str:roomId>", views.chatPage, name="chat-page"),
    path("",views.baseChatPage, name="basechat")
]