# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-08-19 03:45
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import oscar.models.fields.autoslugfield


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='communicationeventtype',
            name='code',
            field=oscar.models.fields.autoslugfield.AutoSlugField(blank=True, editable=False, help_text='Code used for looking up this event programmatically', max_length=128, populate_from='name', separator='_', unique=True, validators=[django.core.validators.RegexValidator(message="Code can only contain the letters a-z, A-Z, digits, and underscores, and can't start with a digit.", regex='^[a-zA-Z_][0-9a-zA-Z_]*$')], verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='productalert',
            name='email',
            field=models.EmailField(blank=True, db_index=True, max_length=254, verbose_name='Email'),
        ),
    ]
