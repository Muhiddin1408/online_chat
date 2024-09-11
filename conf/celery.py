import os
# from __future__ import absolute_import, unicode_literals
# from conf import settings
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')

app = Celery('app')
app.conf.enable_utc = False

app.config_from_object('django.conf:settings', namespace='CELERY')

# Celery Beat settings
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')