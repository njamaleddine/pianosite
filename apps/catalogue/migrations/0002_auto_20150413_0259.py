# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.utility.files


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='product',
            name='artist',
            field=models.ForeignKey(blank=True, to='catalogue.Artist', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='genre',
            field=models.ForeignKey(blank=True, to='catalogue.Genre', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='midi_file',
            field=models.FileField(default=b'', upload_to=apps.utility.files.upload_file, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='sample_audio',
            field=models.URLField(max_length=2048, null=True, blank=True),
            preserve_default=True,
        ),
    ]
