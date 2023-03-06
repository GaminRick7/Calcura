#Imports
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from Calcura import views as vCalc
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

#Urls within the website
urlpatterns = [
    path('', vCalc.Index, name="home"),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('createListing/', vCalc.createListing, name="createListing"),
    path('vendorPage/', vCalc.vendorPage, name="vendorPage"),
    # path("chat/", v.chatPage, name="chat"),
    path("editListing/<int:id>", vCalc.editListing, name="editListing"),
    path("shop/", vCalc.shop, name="shop"),
]
urlpatterns += staticfiles_urlpatterns()