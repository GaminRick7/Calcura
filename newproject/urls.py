from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from calcura import views as v
urlpatterns = [
    path('', v.Index),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
]