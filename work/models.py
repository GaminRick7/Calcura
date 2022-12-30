from django.db import models
from django.contrib.auth.models import User


class calculator(models.Model):
    """
    Table 1 to store calculator listings
    Attributes:
        title (String): the title of a calculator
        price (Float): the price of a calculator
        description (string): the description of a calculator
        tags (string): a string to store the tags of the calculator. Each tag is seperated by a space to store locally within an array
        images (string): a string to store a link to the images. Each image link is seperated by a space to store locally within an array
        user (ForeignKey): a reference to the user who posted the calculator listing
    """
    title = models.TextField(default="")
    price = models.FloatField(default="0.0")
    description = models.TextField(default="")
    tags = models.TextField()
    images = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
