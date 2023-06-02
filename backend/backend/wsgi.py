"""
File: wsgi.py
Authors: Raihaan Sandhu and Darun Kanesalingam
Last Modified: May 19, 2023
Version: 1.0.0

This file contains the WSGI (Web Server Gateway Interface) configurations.
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = get_wsgi_application()
