from django.db import models
from django.contrib.auth.models import User
import datetime

class Messages(models.Model):
    """
    Class to store messages in a room
    Attributes:
        users (str): usernames of people which are in the chat
        id (int): id of the group (created by defalt in django)
    """
    message=models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    roomId = models.TextField()
    datetime = models.DateTimeField(default=datetime.datetime.now())
    id = models.BigAutoField(primary_key=True)
    def __str__(self):
        return f"{self.user}({self.datetime}): {self.message}"

