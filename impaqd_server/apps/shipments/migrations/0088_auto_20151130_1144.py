# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0087_auto_20151125_1835'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shipment',
            name='trip_distance_dirty',
        ),
        migrations.AddField(
            model_name='shipment',
            name='next_trip_dist_update',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 30, 16, 44, 31, 888950, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
