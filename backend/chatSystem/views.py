from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from Calcura.models import MessageRoom, Calculator
from Calcura.views import generateId
from django.http import HttpResponseRedirect
from .models import Messages
@login_required(login_url='/')
def chatPage(request,roomId): #https://www.youtube.com/watch?v=F4nwRQPXD8w&ab_channel=VeryAcademy
    
    a=[]
    email = request.user.email
    count = 0

    for x in MessageRoom.objects.all():
        if email in x.users:
            otherUser = User.objects.get(email=x.users.replace(",","").replace(email, ""))
            a.append([x, otherUser])
            count+=1
    chatsExist = count != 0

    allowedEmails = MessageRoom.objects.get(id=roomId).users.split(",")
    print(allowedEmails)

    if email not in allowedEmails:
        return HttpResponseRedirect("/shop")

    
    



    return render(request, "chat/lobby.html", {"room":roomId, "messages":Messages.objects.filter(roomId=roomId), "chats": a, "length": chatsExist})




