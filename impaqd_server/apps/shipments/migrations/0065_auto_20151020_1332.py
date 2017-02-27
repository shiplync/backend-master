# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import timezone_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0064_auto_20151019_1808'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(max_length=100, null=True, blank=True)),
                ('last_name', models.CharField(max_length=100, null=True, blank=True)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('phone', models.CharField(max_length=20, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ShipmentFeatures',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weight', models.FloatField(null=True, blank=True)),
                ('palletized', models.BooleanField(default=False)),
                ('pallet_number', models.IntegerField(null=True, blank=True)),
                ('pallet_length', models.FloatField(null=True, blank=True)),
                ('pallet_width', models.FloatField(null=True, blank=True)),
                ('pallet_height', models.FloatField(null=True, blank=True)),
                ('extra_details', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ShipmentPayout',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('payout', models.DecimalField(decimal_places=2, default=0, max_digits=9, blank=True, help_text=b'In US dollars', null=True)),
                ('payout_mile', models.DecimalField(decimal_places=2, default=0, max_digits=9, blank=True, help_text=b'In US dollars', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TimeRange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_range_start', models.DateTimeField(null=True, blank=True)),
                ('time_range_end', models.DateTimeField(null=True, blank=True)),
                ('tz', timezone_field.fields.TimeZoneField(default=b'US/Eastern')),
            ],
        ),
        migrations.DeleteModel(
            name='ResponseStatus',
        ),
        migrations.AlterField(
            model_name='equipmenttag',
            name='tag_type',
            field=models.IntegerField(default=1, choices=[(1, b'Flatbed'), (2, b'Van'), (3, b'Reefer'), (4, b'Power Only'), (1000, b'Tarps'), (1002, b'Vented')]),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='receiver',
            field=models.OneToOneField(related_name='incoming_shipments', to='shipments.Location'),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='shipper',
            field=models.OneToOneField(related_name='outgoing_shipments', to='shipments.Location'),
        ),
        migrations.AddField(
            model_name='location',
            name='contact',
            field=models.OneToOneField(null=True, to='shipments.Person'),
        ),
        migrations.AddField(
            model_name='savedlocation',
            name='contact',
            field=models.OneToOneField(null=True, to='shipments.Person'),
        ),
        migrations.AddField(
            model_name='shipment',
            name='delivery_time_info',
            field=models.OneToOneField(related_name='shipment_delivery', null=True, to='shipments.TimeRange'),
        ),
        migrations.AddField(
            model_name='shipment',
            name='features',
            field=models.OneToOneField(null=True, to='shipments.ShipmentFeatures'),
        ),
        migrations.AddField(
            model_name='shipment',
            name='payout_info',
            field=models.OneToOneField(null=True, to='shipments.ShipmentPayout'),
        ),
        migrations.AddField(
            model_name='shipment',
            name='pick_up_time_info',
            field=models.OneToOneField(related_name='shipment_pick_up', null=True, to='shipments.TimeRange'),
        ),
    ]
