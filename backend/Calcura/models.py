from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
import datetime

# Create your models here.
class Calculator(models.Model):
    """
    Calculator listings to be stored within postgresql databse
    Attributes:
        title (str): title of an object
        description (str): description of an object
        image (str): image links seperated by commas for later usage within code, hard to store as a list
        imageNumber (int): amount of images contained for a listing (used for image carousel)
        numImages (int): this won't be stored in database, and is needed since imageNumber is turned into a range when passed to frontend
        price (float): price of an object
        tags (str): tags seperated by double spaces for later usage within code, hard to store as a list
        datetime (datetime): when the listing was created / last modified
        id (int): the id of the int, unique with every listing
        user (ForeignKey): a link to the User table for the user who created the listing
    """
    title = models.TextField()
    description = models.TextField()
    image = models.TextField()
    imageNumber = 0
    numImages = 0
    price = models.DecimalField(decimal_places=2,max_digits=1000)
    tags = models.TextField()
    datetime = models.DateTimeField(default=datetime.datetime.now())
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  

    def __str__(self):
        """
        Magic method to return a string representation of the object
        Args:
            self (Calculator): the object to return representation of
        Returns:
            the string representation of form (title by full name)
        """
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
    locked = models.BooleanField(default=False)
    users=models.TextField()
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user1")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.BigAutoField(primary_key=True)
    latestDateTime = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        """
        Magic method to return a string representation of the MessageRoom
        Returns:
            string in format full name of user1 + fullname of user 2 + roomId
        """
        return f"{self.user1.get_full_name()} and {self.user2.get_full_name()} - {self.id}"

class Favourite(models.Model):
    """
    Class to store messages in a room
    Attributes:
        user (User): the user that owns the favourite
        listing (Calculator): the favourited listing
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.OneToOneField(Calculator, on_delete=models.CASCADE)

class Report(models.Model):
    """
    Class to store all listing reports
    Attributes:
        listing (Calcuator): the reported listing
        description (text): Additional reason
        user (User): the user that reported the listing
    """
    listing = models.ForeignKey(Calculator, on_delete=models.CASCADE)
    description =  models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        """
        Magic method to return a string representation of the object
        Args:
            self (Report): the object to return representation of
        Returns:
            the string representation of form (title by full name)
        """
        return f"{self.listing} | Report by {self.user.get_full_name()}"

class MessageReport(models.Model):
    """
    Class to store all message reports
    Attributes:
        room (MessageRoom): the reported message room
        description (text): Additional reason
        reporter (User): the user that reported the messsage room
        reported (User): the user that is being reported
    """
    room = models.ForeignKey(MessageRoom, on_delete=models.CASCADE)
    description =  models.TextField()
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    reported = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reported")
    def __str__(self):
        """
        Magic method to return a string representation of the object
        Args:
            self (Calculator): the object to return representation of
        Returns:
            the string representation of form (title by full name)
        """
        return f"{self.reported.get_full_name()} | Report by {self.reporter.get_full_name()}"
    