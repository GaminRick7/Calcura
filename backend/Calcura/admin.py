from django.contrib import admin
from .models import Calculator, Administration, MessageRoom

# Registering models so we can access them within django's admin page
admin.site.register(Calculator)
admin.site.register(Administration)
admin.site.register(MessageRoom)