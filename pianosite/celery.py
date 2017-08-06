# -*- coding: utf-8 -*-
import os

from celery import Celery
from dotenv import load_dotenv

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))

# Make sure that we load the env variables so they're available for celery
# This is mainly for development use or environments that use a .env file
load_dotenv(os.path.join(ROOT_DIR, '.env'))

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pianosite.settings")

app = Celery('pianosite')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks()
