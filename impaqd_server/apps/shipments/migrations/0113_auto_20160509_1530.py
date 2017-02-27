# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0112_auto_20160509_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipment',
            name='carrier_assignment',
            field=models.OneToOneField(null=True, blank=True, to='shipments.ShipmentCarrierAssignment'),
        ),
        migrations.AddField(
            model_name='shipment',
            name='driver_assignment',
            field=models.OneToOneField(null=True, blank=True, to='shipments.ShipmentDriverAssignment'),
        ),
    ]
