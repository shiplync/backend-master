# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0113_auto_20160509_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipment',
            name='carrier_assignment',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='shipments.ShipmentCarrierAssignment'),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='driver_assignment',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='shipments.ShipmentDriverAssignment'),
        ),
    ]
