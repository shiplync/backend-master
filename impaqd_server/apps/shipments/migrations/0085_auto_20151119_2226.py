# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0084_auto_20151118_2152'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipment',
            name='first_location',
            field=models.OneToOneField(related_name='shipment_first_location', null=True, blank=True, to='shipments.ShipmentLocation', help_text=b'Read only'),
        ),
        migrations.AddField(
            model_name='shipment',
            name='last_location',
            field=models.OneToOneField(related_name='shipment_last_location', null=True, blank=True, to='shipments.ShipmentLocation', help_text=b'Read only'),
        ),
        migrations.AlterField(
            model_name='shipmentlocation',
            name='shipment',
            field=models.ForeignKey(related_name='locations', to='shipments.Shipment'),
        ),
    ]