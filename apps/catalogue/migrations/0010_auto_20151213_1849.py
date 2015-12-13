# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0009_auto_20151213_1642'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mididownloadurl',
            name='is_valid',
        ),
        migrations.AddField(
            model_name='mididownloadurl',
            name='date_redeemed',
            field=models.DateTimeField(default=None),
            preserve_default=False,
        ),
    ]
