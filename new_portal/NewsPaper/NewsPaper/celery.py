import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')
app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_email_subscribers_week': {
        'task': 'news.tasks.email_week',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}


#Команда для запуска celery на window: celery -A NewsPaper worker -l INFO --pool=solo