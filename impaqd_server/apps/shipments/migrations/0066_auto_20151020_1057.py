# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def forward(apps, schema_editor):
    Shipment = apps.get_model('shipments', 'Shipment')
    Location = apps.get_model('shipments', 'Location')
    SavedLocation = apps.get_model('shipments', 'SavedLocation')
    Person = apps.get_model('shipments', 'Person')
    ShipmentFeatures = apps.get_model('shipments', 'ShipmentFeatures')
    ShipmentPayout = apps.get_model('shipments', 'ShipmentPayout')
    TimeRange = apps.get_model('shipments', 'TimeRange')
    EquipmentTag = apps.get_model('shipments', 'EquipmentTag')
    ContentType = apps.get_model("contenttypes", "ContentType")

    for s in Shipment.objects.all():
        s.features = ShipmentFeatures.objects.create(
            weight=s.weight, palletized=s.palletized,
            pallet_number=s.pallet_number, pallet_length=s.pallet_length,
            pallet_width=s.pallet_width, pallet_height=s.pallet_height,
            extra_details=s.extra_details)
        s.payout_info = ShipmentPayout.objects.create(
            payout=s.payout, payout_mile=s.payout_mile)
        s.pick_up_time_info = TimeRange.objects.create(
            time_range_start=s.pick_up_time_range_start,
            time_range_end=s.pick_up_time_range_end, tz=s.pick_up_tz)
        s.delivery_time_info = TimeRange.objects.create(
            time_range_start=s.delivery_time_range_start,
            time_range_end=s.delivery_time_range_end, tz=s.delivery_tz)
        s.save()
        ct = ContentType.objects.get(model='shipment')
        EquipmentTag.objects.create(
            tag_category=1, tag_type=s.vehicle_type, assignee_content_type=ct,
            assignee_id=s.id, assigner=s.owner_user)

    for l in Location.objects.all():
        l.contact = Person.objects.create(
            email=l.email, phone=l.phone)
        l.save()

    for l in SavedLocation.objects.all():
        l.contact = Person.objects.create(
            email=l.email, phone=l.phone)
        l.save()


def backward(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0065_auto_20151020_1332'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
