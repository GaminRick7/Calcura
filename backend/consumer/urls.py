"""
File: urls.py
Authors: Raihaan Sandhu and Darun Kanesalingam
Last Modified: May 19, 2023
Version: 1.0.0

This file contains the URL routing for the consumer pages.
"""

from consumer import views
from django.urls import path

urlpatterns = [
    path("shop/<int:pageNum>", views.shop, name="shop"),
    path('favourites/', views.favourites, name="favourites"),
]