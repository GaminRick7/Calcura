from django.contrib import admin
from .models import Calculator, Administration, MessageRoom, Favourite, Report, MessageReport
from chatSystem.models import Messages

# Registering models so we can access them within django's admin page

admin.site.register(Calculator)
admin.site.register(Administration)

@admin.action(description='Close Message Room')
def closeMessageRoom(modeladmin, request, queryset):
    queryset.update(locked=True)
    
@admin.action(description='Open Message Room')
def openMessageRoom(modeladmin, request, queryset):
    queryset.update(locked=False)

class MessageInline(admin.TabularInline):
    model = Messages
    extra = 0
    can_delete = True

class MessageRoomAdmin(admin.ModelAdmin):
    actions = [closeMessageRoom, openMessageRoom]
    inlines = [MessageInline]

admin.site.register(MessageRoom, MessageRoomAdmin)
admin.site.register(Favourite)
admin.site.register(Report)
admin.site.register(MessageReport)