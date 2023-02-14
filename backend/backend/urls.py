from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from Calcura import views as vCalc
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from chatSystem import views as vChat
urlpatterns = [
    path('', vCalc.Index, name="home"),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('createListing/', vCalc.createListing, name="createListing"),
    path('vendorPage/', vCalc.vendorPage, name="vendorPage"),
    # path("chat/", v.chatPage, name="chat"),
    path("editListing/<int:id>", vCalc.editListing, name="editListing"),
    path("chat/", include("chatSystem.urls"), name="chat"),
]
urlpatterns += staticfiles_urlpatterns()