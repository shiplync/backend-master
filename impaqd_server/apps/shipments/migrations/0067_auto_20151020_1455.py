# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0066_auto_20151020_1057'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shipment',
            old_name='receiver',
            new_name='delivery_location',
        ),
        migrations.RenameField(
            model_name='shipment',
            old_name='shipper',
            new_name='pick_up_location',
        ),
        migrations.RemoveField(
            model_name='location',
            name='contact_info',
        ),
        migrations.RemoveField(
            model_name='location',
            name='contact_phone',
        ),
        migrations.RemoveField(
            model_name='location',
            name='email',
        ),
        migrations.RemoveField(
            model_name='location',
            name='name',
        ),
        migrations.RemoveField(
            model_name='location',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='savedlocation',
            name='contact_info',
        ),
        migrations.RemoveField(
            model_name='savedlocation',
            name='contact_phone',
        ),
        migrations.RemoveField(
            model_name='savedlocation',
            name='email',
        ),
        migrations.RemoveField(
            model_name='savedlocation',
            name='name',
        ),
        migrations.RemoveField(
            model_name='savedlocation',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='shipment',
            name='delivery_dock',
        ),
        migrations.RemoveField(
            model_name='shipment',
            name='delivery_time_range_end',
        ),
        migrations.RemoveField(
            model_name='shipment',
            name='delivery_time_range_start',
        ),
        migrations.RemoveField(
            model_name='shipment',
            name='delivery_tz',
        ),
        migrations.RemoveField(
            model_name='shipment',
            name='extra_details',
        ),
        migrations.RemoveField(
            model_name='shipment',
            name='pallet_height',
        ),
        migrations.RemoveField(
            model_name='shipment',
            name='pallet_length',
        ),
        migrations.RemoveField(
            model_name='shipment',
            name='pallet_number',
        ),
        migrations.RemoveField(
            model_name='shipment',
            name='pallet_width',
        ),
        migrations.RemoveField(
            model_name='shipment',
            name='palletized',
        ),
        migrations.RemoveField(
            model_name='shipment',
            name='payout',
        ),
        migrations.RemoveField(
            model_name='shipment',
            name='payout_mile',
        ),
        migrations.RemoveField(
            model_name='shipment',
            name='payout_text',
        ),
        migrations.RemoveField(
            model_name='shipment',
            name='pick_up_dock',
        ),
        migrations.RemoveField(
            model_name='shipment',
            name='pick_up_time_range_end',
        ),
        migrations.RemoveField(
            model_name='shipment',
            name='pick_up_time_range_start',
        ),
        migrations.RemoveField(
            model_name='shipment',
            name='pick_up_tz',
        ),
        migrations.RemoveField(
            model_name='shipment',
            name='vehicle_type',
        ),
        migrations.RemoveField(
            model_name='shipment',
            name='weight',
        ),
        migrations.AddField(
            model_name='location',
            name='dock',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='savedlocation',
            name='dock',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
