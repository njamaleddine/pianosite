# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-30 18:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0007_auto_20170430_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gueststripecustomer',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='email address'),
        ),
    ]