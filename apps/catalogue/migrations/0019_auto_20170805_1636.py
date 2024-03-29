# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-05 20:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0018_auto_20170507_1618'),
    ]

    operations = [
        migrations.AddField(
            model_name='productattributevalue',
            name='value_datetime',
            field=models.DateTimeField(blank=True, null=True, verbose_name='DateTime'),
        ),
        migrations.AlterField(
            model_name='productattribute',
            name='type',
            field=models.CharField(choices=[('text', 'Text'), ('integer', 'Integer'), ('boolean', 'True / False'), ('float', 'Float'), ('richtext', 'Rich Text'), ('date', 'Date'), ('datetime', 'Datetime'), ('option', 'Option'), ('multi_option', 'Multi Option'), ('entity', 'Entity'), ('file', 'File'), ('image', 'Image')], default='text', max_length=20, verbose_name='Type'),
        ),
        migrations.AlterUniqueTogether(
            name='productimage',
            unique_together=set([]),
        ),
    ]
