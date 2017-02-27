# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0083_auto_20151117_1542'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shipment',
            name='trip_distance_miles',
        ),
        migrations.RemoveField(
            model_name='shipmentpayout',
            name='payout_mile',
        ),
        migrations.AddField(
            model_name='shipment',
            name='trip_distance_dirty',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='shipmentlocation',
            name='distance_to_next_location',
            field=models.DecimalField(default=0, max_digits=9, decimal_places=1),
        ),
        migrations.AddField(
            model_name='shipmentlocation',
            name='next_location',
            field=models.ForeignKey(related_name='prev_location', blank=True, to='shipments.ShipmentLocation', null=True),
        ),
        migrations.AlterField(
            model_name='shipmentpayout',
            name='payout',
            field=models.DecimalField(default=0, null=True, max_digits=9, decimal_places=2, blank=True),
        ),
    ]
