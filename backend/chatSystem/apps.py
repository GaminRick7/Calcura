from django.apps import AppConfig

#Configure the chatSystem as an app, to be used within settings.py
class ChatsystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chatSystem'
