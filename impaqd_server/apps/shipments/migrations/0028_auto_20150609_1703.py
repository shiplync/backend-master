# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0027_auto_20150602_1557'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shipper',
            name='user',
        ),
        migrations.RemoveField(
            model_name='location',
            name='shipper',
        ),
        migrations.RemoveField(
            model_name='savedlocation',
            name='shipper',
        ),
        migrations.RemoveField(
            model_name='shipment',
            name='shipper_owner',
        ),
        migrations.RemoveField(
            model_name='tosacceptance',
            name='shipper_user',
        ),
        migrations.DeleteModel(
            name='Shipper',
        ),
        migrations.AddField(
            model_name='tosacceptance',
            name='tos_status',
            field=models.IntegerField(default=0, choices=[(0, b'Unset'), (1, b'Accepted'), (2, b'Declined')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tosacceptance',
            name='tos_updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 9, 21, 3, 26, 734040, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tosacceptance',
            name='tos_version',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
    ]
