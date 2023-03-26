from django.urls import path, include
from chatSystem import views 
 
urlpatterns = [
    #Allowing for /chat to have multiple endings, where each ending is a different room
    path("<str:room_name>", views.chatPage, name="chat-page"),
]