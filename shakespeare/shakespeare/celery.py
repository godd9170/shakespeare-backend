import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
# TODO: make sure this is not redundant
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shakespeare.settings.dev')

app = Celery('shakespeare')

app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()