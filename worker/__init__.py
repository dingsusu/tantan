import os
from celery import Celery

from worker import config


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tantan.settings')

celery_app = Celery('tantan')
celery_app.config_from_object(config)
celery_app.autodiscover_tasks()