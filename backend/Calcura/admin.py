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

@admin.action(description='Close Message Room')
def closeMessageRoom(modeladmin, request, queryset):
    queryset.update(locked=True)
    
@admin.action(description='Open Message Room')
def openMessageRoom(modeladmin, request, queryset):
    queryset.update(locked=False)

@admin.action(description='Delete Inactive Rooms')
def deleteInactiveRooms(modeladmin, request, queryset):
    for message in Messages.objects.all():
        print(message)
    for room in MessageRoom.objects.all():

        #If the messageroom is over 30 days old, delete it and its messages
        if (datetime.now(timezone.utc) -   room.latestDateTime).seconds > 60:
            Messages.objects.filter(room=room).delete()
            room.delete()
    
    # MessageRoom.objects.filter(latestDateTime -  >)

class MessageInline(admin.TabularInline):
    model = Messages
    extra = 0
    can_delete = True

class MessageRoomAdmin(admin.ModelAdmin):
    actions = [closeMessageRoom, openMessageRoom, deleteInactiveRooms]
    inlines = [MessageInline]

admin.site.register(MessageRoom, MessageRoomAdmin)
admin.site.register(Favourite)
admin.site.register(Report)
admin.site.register(MessageReport)