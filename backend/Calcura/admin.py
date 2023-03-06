from django.contrib import admin
from .models import Calculator, TempImage

# Registering models so we can acess them within django's admin page
admin.site.register(Calculator)
admin.site.register(TempImage)