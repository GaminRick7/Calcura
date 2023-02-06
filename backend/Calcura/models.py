from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.
class Calculator(models.Model):
    title = models.TextField()
    description = models.TextField()
    image = models.TextField()
    price = models.DecimalField(decimal_places=2,max_digits=1000)
    tags = models.TextField()
    email = models.TextField()

# Temporary model to get cloudinary image url
class TempImage(models.Model):
    image=CloudinaryField('image')
    email=models.TextField()