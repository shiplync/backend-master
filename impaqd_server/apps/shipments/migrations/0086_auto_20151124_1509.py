# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def forward(apps, schema_editor):
    ShipmentLocation = apps.get_model('shipments', 'ShipmentLocation')

    for l in ShipmentLocation.objects.all():
        if l.location_type == 3:
            l.shipment.last_location = l
            l.shipment.save()
        elif l.location_type == 1:
            l.shipment.first_location = l
            l.shipment.save()


def backward(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0085_auto_20151119_2226'),
    ]

    operations = [
    	migrations.RunPython(forward, backward),
    ]