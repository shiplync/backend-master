# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0016_auto_20150501_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='filecontext',
            name='url_ttl',
            field=models.IntegerField(default=30),
            preserve_default=True,
        ),
    ]
