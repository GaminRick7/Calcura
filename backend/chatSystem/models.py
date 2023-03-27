from django.db import models

class Messages(models.Model):
    """
    Class to store messages in a room
    Attributes:
        users (str): usernames of people which are in the chat
        id (int): id of the group (created by defalt in django)
    """
    message=models.TextField()
    user=models.TextField()
    roomId = models.TextField(default="")
    id = models.BigAutoField(primary_key=True)