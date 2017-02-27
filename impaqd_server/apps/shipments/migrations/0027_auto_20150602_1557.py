# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def forward(apps, schema_editor):
    Location = apps.get_model("shipments", "Location")
    SavedLocation = apps.get_model("shipments", "SavedLocation")
    for l in Location.objects.all():
        if l.saved:
            location_name = (
                l.location_name if l.location_name is not None else l.name)
            SavedLocation.objects.create(
                location_name=location_name,
                name=l.name, email=l.email,
                phone=l.phone, address=l.address,
                address_2=l.address_2, zip_code=l.zip_code,
                city=l.city, state=l.state, owner=l.owner,
                coordinate=l.coordinate, contact_info=l.contact_info,
                contact_phone=l.contact_phone)


def backward(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0026_auto_20150601_1237'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
