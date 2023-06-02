"""
File: apps.py
Authors: Raihaan Sandhu and Darun Kanesalingam
Last Modified: May 19, 2023
Version: 1.0.0

This file initializes consumer as a Django app.
"""

from django.apps import AppConfig


class ConsumerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'consumer'
