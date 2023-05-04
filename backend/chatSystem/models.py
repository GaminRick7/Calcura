from django.db import models
from django.contrib.auth.models import User
import datetime
from Calcura.models import MessageRoom

class Messages(models.Model):
    """
    Class to store messages in a room
    Attributes:
        message (str): the message's value
        user (User): User who sent the message
        roomId (str): the id of the room message was sent in
        datetime (datetime): the date and time message was sent
        id (int): the id of the messsage
    """
    message=models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(MessageRoom, on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=datetime.datetime.now())
    id = models.BigAutoField(primary_key=True)

    def __str__(self):
        """
        Magic method to easily represent the message
        Returns:
            F string of the message's representation
        """
        return f"{self.user}({self.datetime}): {self.message}"



