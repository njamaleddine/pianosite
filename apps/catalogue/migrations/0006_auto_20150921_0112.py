# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.utility.toolbelt


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0005_auto_20150921_0045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='midi_file',
            field=models.FileField(max_length=255, upload_to=apps.utility.toolbelt.upload_file),
        ),
    ]
