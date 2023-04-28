from django.contrib import admin
from .models import Calculator, Administration, MessageRoom, MessageRoomMembership


admin.site.register(Calculator)
admin.site.register(Administration)
admin.site.register(MessageRoomMembership)

@admin.action(description='Close Message Room')
def closeMessageRoom(modeladmin, request, queryset):
    queryset.update(locked=True)
@admin.action(description='Open Message Room')
def openMessageRoom(modeladmin, request, queryset):
    queryset.update(locked=False)

class MessageRoomAdmin(admin.ModelAdmin):
    actions = [closeMessageRoom, openMessageRoom]
admin.site.register(MessageRoom, MessageRoomAdmin)