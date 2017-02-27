# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0006_auto_20150401_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrier',
            name='photo',
            field=models.TextField(help_text=b'Photo (encoded as a base64 string)', null=True, blank=True),
            preserve_default=True,
        ),
    ]
