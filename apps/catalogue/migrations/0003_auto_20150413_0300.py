# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.utility.toolbelt


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0002_auto_20150413_0259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='midi_file',
            field=models.FileField(upload_to=apps.utility.toolbelt.upload_file),
            preserve_default=True,
        ),
    ]
