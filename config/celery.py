import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('habit_tracker')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-habit-reminders-every-minute': {
        'task': 'telegram_bot.tasks.send_habit_reminders',
        'schedule': crontab(minute='*'),
    },
    'send-daily-summary': {
        'task': 'telegram_bot.tasks.send_daily_summary',
        'schedule': crontab(hour=20, minute=0),  # Каждый день в 20:00
    },
}

app.conf.timezone = 'Europe/Moscow'
