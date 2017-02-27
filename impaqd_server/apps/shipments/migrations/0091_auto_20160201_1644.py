# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0090_auto_20160128_1156'),
    ]

    operations = [
        migrations.AddField(
            model_name='addressdetails',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 1, 21, 44, 54, 486549, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='addressdetails',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 1, 21, 44, 56, 894595, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
