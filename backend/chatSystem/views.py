from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from Calcura.models import MessageRoom, Calculator, MessageReport
from Calcura.views import generateId
from django.http import HttpResponseRedirect
from .models import Messages

@login_required(login_url='/')
def chatPage(request,roomId): #https://www.youtube.com/watch?v=F4nwRQPXD8w&ab_channel=VeryAcademy
    """
    Function to handle the rooms where people chat in 
    Args:
        request (User): The user who is making the request
        roomId (int): The id of the room which is being accessed
    Returns:
        HttpResponseRedirect to index if either user is not allowed in chat/invalid id is provided
        A render of the page for the user
    """

    #Define variables to be used
    chatList=[]
    email = request.user.email

    #Check if a valid roomId was provided
    if MessageRoom.objects.filter(id=roomId).exists():

        #Gets all message rooms user is in, ordered by most recent (not real time)
        showLatestChats(request.user.email, chatList)
        
        #Get the message room given by the roomId, and the users who are allowed in it
        room = MessageRoom.objects.get(id=roomId)
        allowedEmails = room.users.split(",")
        locked = room.locked

        #If person making request not allowed in room, redirect them
        if email not in allowedEmails:
            return HttpResponseRedirect("/")

        # Get the other user in the room
        otherUser = User.objects.get(email=room.users.replace(",","").replace(email, ""))
        for message in Messages.objects.all():
            print(message.id)
        if request.method=="POST":
            if "report" in request.POST:
                room = MessageRoom.objects.get(id=request.POST['roomid'])
                description = request.POST['description']
                r = MessageReport(room=room, description=description, reporter=request.user, reported=otherUser)
                r.save()
            else:
                id=request.POST["message"]
                if Messages.objects.filter(id=id).exists():
                    Messages.objects.get(id=id).delete()


    else:

        #If not a valid room, return them to index
        return HttpResponseRedirect("/")

    #Returning the template with context
    return render(request, "chat/lobby.html", {"room":roomId, "locked":locked,"messages":Messages.objects.filter(roomId=roomId), "chats": chatList, "otherUser" : otherUser, "roomExists": True})

def baseChatPage(request):
    """
    Function to display the generic /chat/ page to users, which either instructs users to open a chat or tells them they have no chats
    Args:
        request (User): the user who is making the request
    Returns:
        A render of the page for user to see  
    """

    #Defining variables
    chatList=[]
    count=0

    #Looping through all of the 
    count = showLatestChats(request.user.email, chatList)
    roomsExist=count!=0
    return render(request, "chat/lobby.html", {"basePage": True,"chats": chatList, "roomsExist": roomsExist})

def showLatestChats(email, chatList):
    """
    Function get all chats a user is registered in, ordered by most recently a message was sent/chat created
    Args:
        email (str): the email of the user to get chats from
        chatList (list): list to append indices to containing 1. the room 2. the other user in the room
    Returns:
        count (int): amount of rooms user is involved in
    """

    #Define count variable
    count=0

    #Start going through rooms user is in, going by most recent message room
    for room in MessageRoom.objects.filter(users__contains = email).order_by('-latestDateTime'):

        #Find the other user, append an indice to the list and increase count variable
        otherUser = User.objects.get(email=room.users.replace(",","").replace(email, ""))
        chatList.append([room, otherUser])
        count+=1
    return count