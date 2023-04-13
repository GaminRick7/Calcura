from django.urls import path, include
from chatSystem import views 
 
urlpatterns = [
    #Urlpaths for chat rooms and generic chat page
    path("<str:roomId>", views.chatPage, name="chat-page"),
    path("",views.baseChatPage, name="basechat")
]