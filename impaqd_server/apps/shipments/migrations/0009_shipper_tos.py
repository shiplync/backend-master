# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0008_auto_20150402_1019'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipper',
            name='tos',
            field=models.DateTimeField(default=None, null=True),
            preserve_default=True,
        ),
    ]
