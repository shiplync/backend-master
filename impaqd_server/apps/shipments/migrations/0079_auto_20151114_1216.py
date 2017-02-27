# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0078_auto_20151113_1522'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shipment',
            name='delivered_at',
        ),
        migrations.RemoveField(
            model_name='shipment',
            name='delivery_location',
        ),
        migrations.RemoveField(
            model_name='shipment',
            name='delivery_time_info',
        ),
        migrations.RemoveField(
            model_name='shipment',
            name='features',
        ),
        migrations.RemoveField(
            model_name='shipment',
            name='pick_up_location',
        ),
        migrations.RemoveField(
            model_name='shipment',
            name='pick_up_time_info',
        ),
        migrations.RemoveField(
            model_name='shipment',
            name='picked_up_at',
        ),
        migrations.AlterField(
            model_name='shipmentlocation',
            name='shipment',
            field=models.ForeignKey(to='shipments.Shipment'),
        ),
    ]
