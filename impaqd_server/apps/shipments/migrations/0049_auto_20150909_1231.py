# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geolocations', '0007_auto_20150909_1231'),
        ('shipments', '0048_auto_20150909_1122'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carrierdispatcher',
            name='genericuser_ptr',
        ),
        migrations.DeleteModel(
            name='CarrierDispatcher',
        ),
        migrations.RemoveField(
            model_name='carrierdriver',
            name='genericuser_ptr',
        ),
        migrations.RemoveField(
            model_name='shipperlogisticsmanager',
            name='genericuser_ptr',
        ),
        migrations.DeleteModel(
            name='ShipperLogisticsManager',
        ),
        migrations.AlterField(
            model_name='shipmentrequest',
            name='driver',
            field=models.ForeignKey(blank=True, to='shipments.GenericUser', null=True),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='CarrierDriver',
        ),
    ]
