from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from Calcura.models import MessageRoom, Calculator
from Calcura.views import generateId, findTopMessageRoom
from django.http import HttpResponseRedirect
from .models import Messages
@login_required(login_url='/')
def chatPage(request,roomId): #https://www.youtube.com/watch?v=F4nwRQPXD8w&ab_channel=VeryAcademy
    
    a=[]
    email = request.user.email
    count = 0

    for x in MessageRoom.objects.filter(user1=request.user).order_by('-datetime'):
        otherUser = x.user2
        a.append([x, otherUser])
        count+=1

    for x in MessageRoom.objects.filter(user2=request.user).order_by('-datetime'):
        otherUser = x.user1
        a.append([x, otherUser])
        count+=1
    chatsExist = count != 0

    room = MessageRoom.objects.get(id=roomId)
    allowedEmails = room.users.split(",")
    otherUser = User.objects.get(email=room.users.replace(",","").replace(email, ""))
    print(allowedEmails)

    if email not in allowedEmails:
        return HttpResponseRedirect("/shop")

    
    



    return render(request, "chat/lobby.html", {"room":roomId, "messages":Messages.objects.filter(roomId=roomId), "chats": a, "length": chatsExist, "otherUser" : otherUser, 'message': findTopMessageRoom(request.user)})
