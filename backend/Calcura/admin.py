from django.contrib import admin
from .models import Calculator, Administration, MessageRoom


# Registering models so we can access them within django's admin page
admin.site.register(Calculator)
admin.site.register(Administration)

@admin.action(description='Close Message Room')
def closeMessageRoom(modeladmin, request, queryset):
    queryset.update(locked=True)
@admin.action(description='Open Message Room')
def openMessageRoom(modeladmin, request, queryset):
    queryset.update(locked=False)

class MessageRoomAdmin(admin.ModelAdmin):
    actions = [closeMessageRoom, openMessageRoom]

admin.site.register(MessageRoom, MessageRoomAdmin)