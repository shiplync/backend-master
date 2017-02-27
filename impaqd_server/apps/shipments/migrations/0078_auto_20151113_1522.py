# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def forward(apps, schema_editor):
    ShipmentLocation = apps.get_model('shipments', 'ShipmentLocation')
    ShipmentFeatures = apps.get_model('shipments', 'ShipmentFeatures')

    for l in ShipmentLocation.objects.all():
        if hasattr(l, 'incoming_shipments'):
            l.shipment = l.incoming_shipments
            l.location_type = 3
            l.time_range = l.incoming_shipments.delivery_time_info
            l.features = ShipmentFeatures.objects.create()
            l.arrival_time = l.incoming_shipments.delivered_at
            l.save()
        elif hasattr(l, 'outgoing_shipments'):
            l.shipment = l.outgoing_shipments
            l.location_type = 1
            l.time_range = l.outgoing_shipments.pick_up_time_info
            l.features = l.outgoing_shipments.features
            l.arrival_time = l.outgoing_shipments.picked_up_at
            l.save()
        else:
            l.delete()


def backward(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0077_auto_20151113_1507'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
