from __future__ import absolute_import, unicode_literals

import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Taxi_bot.settings')

app = Celery('Taxi_bot')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.timezone   = 'Asia/Tashkent'
app.conf.enable_utc   = True

app.conf.beat_schedule = {
    'main-worker': {
        'task': 'Bot.tasks.clear_expired_ads',
        'schedule': crontab(minute=1, hour=0),
    },
}


app.autodiscover_tasks()
