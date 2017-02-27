# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def forward(apps, schema_editor):
    BasePermission = apps.get_model('shipments', 'BasePermission')
    BasePermissionCollection = apps.get_model('shipments', 'BasePermissionCollection')

    for b in BasePermission.objects.all():
        b.delete()

    for b in BasePermissionCollection.objects.all():
        b.delete()

def backward(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('geolocations', '0006_auto_20150902_1635'),
        ('shipments', '0044_auto_20150902_1635'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carriercompany',
            name='genericcompany_ptr',
        ),
        migrations.DeleteModel(
            name='CarrierCompany',
        ),
        migrations.RemoveField(
            model_name='shippercompany',
            name='genericcompany_ptr',
        ),
        migrations.DeleteModel(
            name='ShipperCompany',
        ),
        migrations.RunPython(forward, backward),
    ]
