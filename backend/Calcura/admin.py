from django.contrib import admin
from .models import Calculator, Administration, MessageRoom, Favourite, Report, MessageReport
from chatSystem.models import Messages
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from django.contrib import admin
from django.utils import timezone

# Registering models so we can access them within django's admin page
admin.site.register(Calculator)
admin.site.register(Administration)

#Creating actions

@admin.action(description='Close Message Room')
def closeMessageRoom(modeladmin, request, queryset):
    """
    Close/Lock a message room in django
    Args:
        modeladmin: representation of a model in the admin interface
        request: user making the request
        queryset: the queryset to deal with sent by user making the request
    """
    queryset.update(locked=True)
    
@admin.action(description='Open Message Room')
def openMessageRoom(modeladmin, request, queryset):
    """
    Open the message room after it was locked
    Args:
        modeladmin: representation of a model in the admin interface
        request: user making the request
        queryset: the queryset to deal with sent by user making the request
    """
    queryset.update(locked=False)

@admin.action(description='Delete Inactive Rooms')
def deleteInactiveRooms(modeladmin, request, queryset):
    """
    Delete rooms which haven't been used in 30 days
    Args:
        modeladmin: representation of a model in the admin interface
        request: user making the request
        queryset: the queryset to deal with sent by user making the request
    """
    for message in Messages.objects.all():
        print(message)
    for room in MessageRoom.objects.all():

        #If the messageroom is over 30 days old, delete it and its messages
        if (datetime.now(timezone.utc) -   room.latestDateTime).seconds > 2592000:
            Messages.objects.filter(room=room).delete()
            room.delete()

class MessageInline(admin.TabularInline):
    """
    Class to allow messages to be shown inline within a messageroom in admin page
    """
    model = Messages
    extra = 0
    can_delete = True

class MessageRoomAdmin(admin.ModelAdmin):
    """
    Define the actions and any inlines within the MessageRoom view in admin page
    """
    actions = [closeMessageRoom, openMessageRoom, deleteInactiveRooms]
    inlines = [MessageInline]


#Registering models to be viewed in admin page
admin.site.register(MessageRoom, MessageRoomAdmin)
admin.site.register(Favourite)
admin.site.register(Report)
admin.site.register(MessageReport)