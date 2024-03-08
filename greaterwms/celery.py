import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'greaterwms.settings')

from django.conf import settings
from celery import platforms
from celery import Celery
app = Celery(f"application", include=['utils.makepdf'])
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
platforms.C_FORCE_ROOT = True
