import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Messages
import os
import django

#Allowing sync operations to run in an async setting
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

async def saveItems(self,message,user):
    toSave=Messages(message=message,user=user,roomId=self.scope['url_route']['kwargs']['room_name'])
    toSave.save()

class ChatConsumer(AsyncWebsocketConsumer):
    """
    Class to create destroy and modify Websockets. Groups are the area which many users can store. The channel is how data is sent. 
    Attributes:
        roomGroupName (str): the group name which the consumer is in
        channel_name (str): the name of the channel the user is in
        channel_layer (str): the layer of the channel which the user is in

    """

    #When a websocket connection is created or a connection has been opened, creates a groupname for chat and adds it to the channel layer
    async def connect(self):

        #Setting the groupname to the items after the /
        self.roomGroupName = self.scope['url_route']['kwargs']['room_name']
        await self.channel_layer.group_add(
            self.roomGroupName ,
            self.channel_name
        )
        await self.accept()
    
    #Removes the instamce from the group
    async def disconnect(self , close_code):
        await self.channel_layer.group_discard(
            self.roomGroupName ,
            self.channel_layer
        )

    #Triggered when sending data from the websocket
    async def receive(self, text_data):

        #Retreive the text data, the message and username of person who sent message
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        print(self.scope['url_route']['kwargs']['room_name'])
        
        toSave=Messages(message=message,user=username,roomId=self.scope['url_route']['kwargs']['room_name'])
        toSave.save()
        
        #Spread the message to other users in the chatroom with the sendMessage function defined right below
        await self.channel_layer.group_send(
            self.roomGroupName,{
                "type" : "sendMessage" ,
                "message" : message ,
                "username" : username ,
            })

    #Takes the user which is sending data and then holds it. It then sends the message and user to all instances in group. 
    async def sendMessage(self , event) :
        message = event["message"]
        username = event["username"]
        await self.send(text_data = json.dumps({"message":message ,"username":username}))
