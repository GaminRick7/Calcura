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

    if MessageRoom.objects.filter(id=roomId).exists():
        #Gets all message rooms user is in
        for x in MessageRoom.objects.filter(users__contains = email).order_by('-latestDateTime'):
            tempOtherUser = User.objects.get(email=x.users.replace(",","").replace(email, ""))
            print(x.latestDateTime,tempOtherUser)
            a.append([x, tempOtherUser])
            count+=1


        chatsExist = count != 0
        room = MessageRoom.objects.get(id=roomId)
        allowedEmails = room.users.split(",")

        if email not in allowedEmails:
            return HttpResponseRedirect("../")

        otherUser = User.objects.get(email=room.users.replace(",","").replace(email, ""))
        print(allowedEmails)
    else:
        return HttpResponseRedirect("/")



    
    



    return render(request, "chat/lobby.html", {"room":roomId, "messages":Messages.objects.filter(roomId=roomId), "chats": a, "length": chatsExist, "otherUser" : otherUser, 'message': findTopMessageRoom(request.user)})




