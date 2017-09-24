# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    """
    no-op because this migration was changed into a management command instead
    """
    dependencies = [
        ('promotions', '0001_initial'),  # We need django-oscar to create the db table schema first
        ('catalogue', '0006_auto_20150921_0112'),
    ]
    operations = []
