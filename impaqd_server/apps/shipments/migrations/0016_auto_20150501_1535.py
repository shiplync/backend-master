# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0015_auto_20150427_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genericcompany',
            name='company_name',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shipment',
            name='delivery_status',
            field=models.IntegerField(default=1, choices=[(1, b'Open'), (2, b'Pending Pickup'), (3, b'Enroute'), (4, b'Delivered'), (5, b'Pending Approval')]),
            preserve_default=True,
        ),
    ]
