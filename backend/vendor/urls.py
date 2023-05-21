#Imports
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from vendor import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from chatSystem import urls as chatUrls
from django.views.generic import TemplateView

#Urls within the website
urlpatterns = [
    path('createListing/', views.createListing, name="createListing"),
    path('vendorPage/', views.vendorPage, name="vendorPage"),
    path("editListing/<int:id>", views.editListing, name="editListing"),
]