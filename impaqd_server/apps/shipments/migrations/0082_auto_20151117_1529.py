# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def forward(apps, schema_editor):
    ShipmentLocation = apps.get_model('shipments', 'ShipmentLocation')
    SavedLocation = apps.get_model('shipments', 'SavedLocation')
    AddressDetails = apps.get_model('shipments', 'AddressDetails')

    for l in ShipmentLocation.objects.all():
        l.address_details = AddressDetails.objects.create(
            address=l.address, address_2=l.address_2, zip_code=l.zip_code,
            city=l.city, state=l.state, coordinate=l.coordinate)
        l.save()

    for l in SavedLocation.objects.all():
        l.address_details = AddressDetails.objects.create(
            address=l.address, address_2=l.address_2, zip_code=l.zip_code,
            city=l.city, state=l.state, coordinate=l.coordinate)    
        l.save()


def backward(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0081_auto_20151117_1528'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
