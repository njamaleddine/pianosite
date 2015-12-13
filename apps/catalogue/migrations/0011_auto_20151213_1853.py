# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0010_auto_20151213_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mididownloadurl',
            name='date_redeemed',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
