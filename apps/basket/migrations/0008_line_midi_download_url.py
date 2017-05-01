# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2016-11-12 20:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0015_mididownloadurl_downloads_left'),
        ('basket', '0007_slugfield_noop'),
    ]

    operations = [
        migrations.AddField(
            model_name='line',
            name='midi_download_url',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalogue.MidiDownloadURL'),
        ),
    ]
