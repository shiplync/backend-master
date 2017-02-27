# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0034_auto_20150618_1757'),
    ]

    operations = [
        migrations.AddField(
            model_name='globalsettings',
            name='current_tos_version',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
