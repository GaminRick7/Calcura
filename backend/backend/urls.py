#Imports
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from Calcura import views as vCalc
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from chatSystem import urls as chatUrls
from django.views.generic import TemplateView
from vendor import urls as vendorUrls
from consumer import urls as consumerUrls

#Urls within the website
urlpatterns = [
    path('', vCalc.Index, name="home"),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('chat/', include(chatUrls)),
    path('', include(vendorUrls)),
    path('',include(consumerUrls)),
    path('contact/', vCalc.contact, name="contact"),
    path('faq/', TemplateView.as_view(template_name="calcura/faq.html"), name="faq"),
]
urlpatterns += staticfiles_urlpatterns()