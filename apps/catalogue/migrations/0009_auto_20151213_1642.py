# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0008_auto_20151213_1611'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mididownloadurl',
            name='id',
        ),
        migrations.AddField(
            model_name='mididownloadurl',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 13, 16, 42, 19, 441109, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mididownloadurl',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 13, 16, 42, 24, 840584, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='mididownloadurl',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True),
        ),
    ]
