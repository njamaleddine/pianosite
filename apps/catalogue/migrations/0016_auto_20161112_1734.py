# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2016-11-12 22:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0015_mididownloadurl_downloads_left'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mididownloadurl',
            name='downloads_left',
            field=models.IntegerField(default=2),
        ),
    ]
