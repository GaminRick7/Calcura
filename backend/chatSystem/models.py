from django.db import models

class Message(models.Model):
    text = models.TextField()
    sender = models.CharField(max_length=255)
    time = models.DateTimeField(auto_now_add=True)
    room = models.TextField()