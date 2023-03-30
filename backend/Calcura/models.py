from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from chatSystem.models import Messages
import datetime

# Create your models here.
class Calculator(models.Model):
    """
    Calculator listings to be stored within postgresql databse
    Attributes:
        title (str): title of an object
        description (str): description of an object
        image (str): image links seperated by commas for later usage within code, hard to store as a list
        price (float): price of an object
        tags (str): tags seperated by double spaces for later usage within code, hard to store as a list
        email (str): email address of object's poster. Email addresses are unique within ocdsb so allows us to link an object to a client
        fullname (str): full name of the poster. Used within shop page to show who owns a listing
    """
    title = models.TextField()
    description = models.TextField()
    image = models.TextField()
    price = models.DecimalField(decimal_places=2,max_digits=1000)
    tags = models.TextField()
    # email = models.TextField()
    # fullname = models.TextField()
    datetime = models.DateTimeField(default=datetime.datetime.now())
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    

    def __str__(self):
        return f"{self.title} by {self.user.get_full_name()}"
    

class TempImage(models.Model):
    """
    Model to get cloudinary image url
    Attributes:
        image (CloudinaryField): the image being uploaded to cloudinary
        email (str): email address of person who is uploading image for a listing. Email addresses need to differentiate listings in case multiple people upload a listing at same time.  
    """
    image=CloudinaryField('image')
    email=models.TextField()

class Administration(models.Model):
    """
    Model for administrators to control website/get key data
    Attributes:
        tags: (str) all tags currently in use
    """
    tags=models.TextField(default="Texas Instruments,Sharp,Casio,New,Used")

class MessageRoom(models.Model):
    """
    Class to hold message rooms between a consumer and a vendor
    Attributes:
        users (str): usernames of people which are in the chat
        id (int): id of the group (created by defalt in django)
    """

    users=models.TextField()
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, default=User.objects.first().pk, related_name="user1")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, default=User.objects.first().pk)
    id = models.BigAutoField(primary_key=True)
    messages = models.ManyToManyField(Messages, limit_choices_to={'roomId': id})
    message=Messages.objects.all()
    for m in message:
        print(m.roomId,type(m.roomId))
        print(m.roomId==id)
        print(str(id),"im gay i suck dick")
        print(m.roomId==id)

    print(type(str(id)))
    print("im raihaan and im gay")
    def __str__(self):
        return f"{self.user1.get_full_name()} and {self.user2.get_full_name()} - {self.id}"