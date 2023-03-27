from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Calcura.models import MessageRoom, Calculator
from django.http import HttpResponseRedirect
from .models import Messages
@login_required(login_url='/')
def chatPage(request,room_name): #https://www.youtube.com/watch?v=F4nwRQPXD8w&ab_channel=VeryAcademy
    
    allowedUsers = MessageRoom.objects.get(id=room_name).users.split(",")
    if request.user.get_full_name() not in allowedUsers:
        return HttpResponseRedirect("/shop")
    
    for i in Messages.objects.all():
        print(i.message)




    return render(request, "chat/lobby.html", {"room":room_name})




