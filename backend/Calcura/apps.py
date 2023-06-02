"""
File: apps.py
Authors: Raihaan Sandhu and Darun Kanesalingam
Last Modified: February 7, 2023
Version: 1.0.0

This file initializes Calcura as a Django app.
"""

from django.apps import AppConfig


class CalcuraConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Calcura'
