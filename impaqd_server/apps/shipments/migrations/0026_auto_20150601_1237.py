# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0025_auto_20150528_1039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrier',
            name='vehicle_type',
            field=models.IntegerField(default=1, null=True, blank=True, choices=[(1, b'Flatbed'), (2, b'Reefer'), (3, b'Van'), (4, b'Power Only')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='genericuser',
            name='vehicle_type',
            field=models.IntegerField(default=1, null=True, blank=True, choices=[(1, b'Flatbed'), (2, b'Reefer'), (3, b'Van'), (4, b'Power Only')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='location',
            name='contact_phone',
            field=models.CharField(help_text='The phone number of the person to         contact on the shipper/receiver side', max_length=20, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='savedlocation',
            name='contact_phone',
            field=models.CharField(help_text='The phone number of the person to         contact on the shipper/receiver side', max_length=20, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shipment',
            name='delivery_status',
            field=models.IntegerField(default=1, choices=[(1, b'Open'), (2, b'PendingPickup'), (3, b'Enroute'), (4, b'Delivered'), (5, b'Pending Approval')]),
            preserve_default=True,
        ),
    ]
