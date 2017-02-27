# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


def forward(apps, schema_editor):
    CarrierDriver = apps.get_model('shipments', 'carrierdriver')
    GenericUser = apps.get_model('shipments', 'genericuser')
    for u in GenericUser.objects.all():
        if hasattr(u, 'carrierdriver'):
            u.last_location = u.carrierdriver.last_location2
            u.last_location_timestamp = u.carrierdriver.last_location_timestamp2
            u.vehicle_type = u.carrierdriver.vehicle_type2
            u.save()

def backward(apps, schema_editor):
    CarrierDriver = apps.get_model('shipments', 'carrierdriver')
    GenericUser = apps.get_model('shipments', 'genericuser')
    for u in GenericUser.objects.all():
        if hasattr(u, 'carrierdriver'):
            u.carrierdriver.last_location2 = u.last_location
            u.carrierdriver.last_location_timestamp2 = u.last_location_timestamp
            u.carrierdriver.vehicle_type2 = u.vehicle_type

class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0021_auto_20150519_1810'),
    ]

    operations = [
        migrations.RenameField(
            model_name='carrierdriver',
            old_name='last_location',
            new_name='last_location2',
        ),
        migrations.RenameField(
            model_name='carrierdriver',
            old_name='last_location_timestamp',
            new_name='last_location_timestamp2',
        ),
        migrations.RenameField(
            model_name='carrierdriver',
            old_name='vehicle_type',
            new_name='vehicle_type2',
        ),
        migrations.AddField(
            model_name='genericuser',
            name='last_location',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, geography=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='genericuser',
            name='last_location_timestamp',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='genericuser',
            name='vehicle_type',
            field=models.IntegerField(default=1, null=True, blank=True, choices=[(1, b'Flatbed'), (2, b'Reefer'), (3, b'Van'), (4, b'Power only')]),
            preserve_default=True,
        ),
        migrations.RunPython(forward, backward),
        migrations.RemoveField(
            model_name='carrierdriver',
            name='last_location2',
        ),
        migrations.RemoveField(
            model_name='carrierdriver',
            name='last_location_timestamp2',
        ),
        migrations.RemoveField(
            model_name='carrierdriver',
            name='vehicle_type2',
        ),
    ]
