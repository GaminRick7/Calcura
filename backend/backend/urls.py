from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from Calcura import views as v
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', v.Index, name="home"),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('createListing/', v.createListing, name="createListing"),
    path('vendorPage/', v.vendorPage, name="vendorPage"),
    path("chat/", v.chatPage, name="chat"),
    path("editListing/<int:id>", v.editListing, name="editListing"),
]
urlpatterns += staticfiles_urlpatterns()