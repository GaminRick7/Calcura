import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Messages
from Calcura.models import MessageRoom
import os
import django
import re
from django.contrib.auth.models import User
from Calcura.views import generateId
import datetime

#Allowing sync operations to run in an async setting (saving messages won't be allowed otherwise)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

async def saveItems(self,message,user):
    """
    Function to save message object to Messages table
    Args:
        message (str): the value of the message which was sent
        user (User): the user who sent the message
    """

    #Creating the message object then saving it to db
    toSave=Messages(message=message,user=User.objects.filter(email=user).get(),roomId=self.scope['url_route']['kwargs']['roomId'], datetime= datetime.datetime.now(),id=generateId(Messages))
    toSave.save()
    messageRoom=MessageRoom.objects.get(id=self.scope['url_route']['kwargs']['roomId'])
    messageRoom.messages.add(toSave)


class ChatConsumer(AsyncWebsocketConsumer):
    """
    Class to create destroy and modify Websockets. Groups are the area which many users can store. The channel is how data is sent. 
    Attributes:
        roomGroupName (str): the group name which the consumer is in
        channel_name (str): the name of the channel the user is in
        channel_layer (str): the layer of the channel which the user is in
    """

    #Getting a list of bad words to filter with
    outfile = open("chatSystem/badwords.txt", "r")
    badWordsList=list(outfile)
    for i in range(len(badWordsList)):
        badWordsList[i]=badWordsList[i][:-1]
    outfile.close()

    #When a websocket connection is created or a connection has been opened, creates a groupname for chat and adds it to the channel layer
    async def connect(self):

        #Setting the groupname to the id after the [domain]/chat/
        self.roomGroupName = self.scope['url_route']['kwargs']['roomId']

        #Adding the group to the channel
        await self.channel_layer.group_add(
            self.roomGroupName ,
            self.channel_name
        )
        await self.accept()
    
    #Removes the user from the group when chat page & connection is closed
    async def disconnect(self , close_code):
        await self.channel_layer.group_discard(
            self.roomGroupName ,
            self.channel_layer
        )

    #Triggered when receiving data from the websocket
    async def receive(self, text_data):

        #Retreive the text data, the message and username of person who sent message
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        email = text_data_json["email"]

        #Update the datetime value in the message room from which the message belongs to
        MessageRoom.objects.filter(id=self.scope['url_route']['kwargs']['roomId']).update(latestDateTime=datetime.datetime.now())

        #Filtering any bad words
        if message!="":
            #For all the bad words in the list
            for badWord in self.badWordsList:
                #If a bad word is in the message 
                if badWord.lower() in message.lower():
                    #Split the message into a list of words
                    message = message.split(" ")
                    
                    #Query through the list of words
                    for i in range(len(message)):

                        #If the bad word is in the word
                        if badWord.lower() in message[i].lower():
                            
                            #Replace the bad word with '*'
                            message[i] = message[i].lower().replace(badWord.lower(), "*"*len(badWord))
                            
                    #Finally, turn the message BACK into a string once filtering is completed
                    message=" ".join(message)
                    
            #Spread the message to other users in the chatroom with the sendMessage function defined right below
            await self.channel_layer.group_send(
                self.roomGroupName,{
                    "type" : "sendMessage" ,
                    "message" : message ,
                    "email" : email ,
                })
            
            #Saving message to db
            await saveItems(self,message,email)

    #Takes the user which is sending data and then holds it. It then sends the message and user to all instances in group. 
    async def sendMessage(self , event) :
        message = event["message"]
        email = event["email"]
        await self.send(text_data = json.dumps({"message":message ,"email":email, "fullname" : User.objects.filter(email=email).get().get_full_name()}))
