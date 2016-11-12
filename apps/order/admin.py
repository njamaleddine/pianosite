# -*- coding: utf-8 -*-
from django.contrib import admin

from django.apps import apps


for model in apps.get_app_config('order').models.values():
    admin.site.register(model)
