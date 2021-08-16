"""
WSGI config for Taxi_bot project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import locale
import os

from django.core.wsgi import get_wsgi_application

locale.setlocale(locale.LC_ALL, 'uz_UZ.UTF-8')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Taxi_bot.settings')

application = get_wsgi_application()
