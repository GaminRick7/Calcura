from consumer import views
from django.urls import path

urlpatterns = [
    path("shop/<int:pageNum>", views.shop, name="shop"),
    path('favourites/', views.favourites, name="favourites"),
]