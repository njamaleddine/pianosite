# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalogue', '0004_auto_20150913_2058'),
    ]

    operations = [
        migrations.CreateModel(
            name='MidiDownloadURL',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('is_valid', models.BooleanField(default=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='full_audio',
            field=models.URLField(max_length=2048, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='mididownloadurl',
            name='product',
            field=models.ForeignKey(to='catalogue.Product'),
        ),
    ]
