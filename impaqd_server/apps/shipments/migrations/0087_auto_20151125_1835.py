# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0086_auto_20151124_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipment',
            name='first_location',
            field=models.OneToOneField(related_name='shipment_first_location', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='shipments.ShipmentLocation', help_text=b'Read only'),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='last_location',
            field=models.OneToOneField(related_name='shipment_last_location', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='shipments.ShipmentLocation', help_text=b'Read only'),
        ),
        migrations.AlterField(
            model_name='shipmentlocation',
            name='next_location',
            field=models.ForeignKey(related_name='prev_location', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='shipments.ShipmentLocation', null=True),
        ),
    ]
