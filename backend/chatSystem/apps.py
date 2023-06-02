"""
File: apps.py
Authors: Raihaan Sandhu and Darun Kanesalingam
Last Modified: April 13, 2023
Version: 1.0.0

This file initializes chatSystem as a Django app.
"""

from django.apps import AppConfig

#Configure the chatSystem as an app, to be used within settings.py
class ChatsystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chatSystem'
