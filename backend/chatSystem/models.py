from django.db import models
import datetime

class Messages(models.Model):
    """
    Class to store messages in a room
    Attributes:
        users (str): usernames of people which are in the chat
        id (int): id of the group (created by defalt in django)
    """
    message=models.TextField()
    user=models.TextField()
    roomId = models.TextField()
    datetime = models.DateTimeField(default=datetime.datetime.now())
    id = models.BigAutoField(primary_key=True)