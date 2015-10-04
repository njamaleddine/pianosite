from django.contrib import admin

# from django.db.models import get_models, get_app
from django.apps import apps


for model in apps.get_app_config('checkout').models.values():
    admin.site.register(model)
