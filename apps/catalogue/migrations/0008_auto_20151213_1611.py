# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import apps.utility.files


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0007_auto_20151004_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='full_audio',
            field=models.FileField(max_length=1024, null=True, upload_to=apps.utility.files.upload_file, blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='midi_file',
            field=models.FileField(max_length=1024, upload_to=apps.utility.files.upload_file),
        ),
        migrations.AlterField(
            model_name='product',
            name='sample_audio',
            field=models.FileField(max_length=1024, null=True, upload_to=apps.utility.files.upload_file, blank=True),
        ),
    ]
