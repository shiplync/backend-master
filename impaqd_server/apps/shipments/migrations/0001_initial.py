# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields
from django.conf import settings
import timezone_field.fields
import impaqd_server.apps.shipments.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_tester', models.BooleanField(default=False, help_text='Is this a real trucker or someone who has been granted access to the app for other purposes.')),
                ('first_name', models.CharField(default=b'', max_length=100, null=True, blank=True)),
                ('last_name', models.CharField(default=b'', max_length=100, null=True, blank=True)),
                ('phone', models.CharField(default=b'', max_length=20, null=True, blank=True)),
                ('email', models.EmailField(unique=True, max_length=75)),
                ('photo', models.TextField(help_text=b'Photo (encoded as a base64 string)')),
                ('mcdot', models.CharField(max_length=32, verbose_name=b'USDOT')),
                ('app_pin', models.CharField(default=b'0000', max_length=10)),
                ('verified', models.BooleanField(default=False)),
                ('rejected', models.BooleanField(default=False)),
                ('last_location', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, geography=True, blank=True)),
                ('last_location_timestamp', models.DateTimeField(null=True, blank=True)),
                ('vehicle_type', models.IntegerField(default=1, null=True, blank=True, choices=[(1, b'Flatbed'), (2, b'Reefer'), (3, b'Van'), (4, b'Power only')])),
                ('device_token', models.CharField(default=b'', max_length=256, null=True, help_text=b'for IOS devices', blank=True)),
                ('platform', models.IntegerField(default=1, null=True, blank=True, choices=[(1, b'Unknown'), (2, b'iOS'), (3, b'Android'), (4, b'Web')])),
                ('allow_notifications', models.BooleanField(default=True)),
                ('user', models.OneToOneField(null=True, default=None, blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=75, null=True, blank=True)),
                ('phone', models.CharField(max_length=20)),
                ('address', models.TextField()),
                ('address_2', models.TextField(null=True, blank=True)),
                ('zip_code', models.CharField(blank=True, max_length=5, null=True, validators=[impaqd_server.apps.shipments.validators.validate_zip_code])),
                ('city', models.CharField(max_length=50, null=True, blank=True)),
                ('state', models.CharField(blank=True, max_length=2, null=True, choices=[(b'AL', b'ALABAMA'), (b'AK', b'ALASKA'), (b'AZ', b'ARIZONA'), (b'AR', b'ARKANSAS'), (b'CA', b'CALIFORNIA'), (b'CO', b'COLORADO'), (b'CT', b'CONNECTICUT'), (b'DE', b'DELAWARE'), (b'FL', b'FLORIDA'), (b'GA', b'GEORGIA'), (b'HI', b'HAWAII'), (b'ID', b'IDAHO'), (b'IL', b'ILLINOIS'), (b'IN', b'INDIANA'), (b'IA', b'IOWA'), (b'KS', b'KANSAS'), (b'KY', b'KENTUCKY'), (b'LA', b'LOUISIANA'), (b'ME', b'MAINE'), (b'MD', b'MARYLAND'), (b'MA', b'MASSACHUSETTS'), (b'MI', b'MICHIGAN'), (b'MN', b'MINNESOTA'), (b'MS', b'MISSISSIPPI'), (b'MO', b'MISSOURI'), (b'MT', b'MONTANA'), (b'NE', b'NEBRASKA'), (b'NV', b'NEVADA'), (b'NH', b'NEW HAMPSHIRE'), (b'NJ', b'NEW JERSEY'), (b'NM', b'NEW MEXICO'), (b'NY', b'NEW YORK'), (b'NC', b'NORTH CAROLINA'), (b'ND', b'NORTH DAKOTA'), (b'OH', b'OHIO'), (b'OK', b'OKLAHOMA'), (b'OR', b'OREGON'), (b'PA', b'PENNSYLVANIA'), (b'RI', b'RHODE ISLAND'), (b'SC', b'SOUTH CAROLINA'), (b'SD', b'SOUTH DAKOTA'), (b'TN', b'TENNESSEE'), (b'TX', b'TEXAS'), (b'UT', b'UTAH'), (b'VT', b'VERMONT'), (b'VA', b'VIRGINIA'), (b'WA', b'WASHINGTON'), (b'WV', b'WEST VIRGINIA'), (b'WI', b'WISCONSIN'), (b'WY', b'WYOMING')])),
                ('coordinate', django.contrib.gis.db.models.fields.PointField(srid=4326, geography=True)),
                ('contact_info', models.CharField(help_text='E.g. name of contact', max_length=100, blank=True)),
                ('contact_phone', models.CharField(help_text='The phone number of the person to contact on the shipper/receiver side', max_length=20, blank=True)),
                ('saved', models.BooleanField(default=False, help_text='Whether or not the user has saved the location')),
                ('hash_key', models.CharField(help_text=b'SHA 256 hash value to prevent duplicate entries', max_length=64, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Shipment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('shipment_id', models.CharField(help_text=b'Identifier for shipment. Not same as database primary key.', max_length=32, null=True, blank=True)),
                ('payout', models.DecimalField(decimal_places=2, default=0, max_digits=9, blank=True, help_text=b'In US dollars', null=True)),
                ('payout_mile', models.DecimalField(decimal_places=2, default=0, max_digits=9, blank=True, help_text=b'In US dollars', null=True)),
                ('payout_text', models.CharField(help_text='E.g. if rate is pr. mile. Dont need payout as well', max_length=100, blank=True)),
                ('vehicle_type', models.IntegerField(choices=[(1, b'Flatbed'), (2, b'Reefer'), (3, b'Van'), (4, b'Power Only')])),
                ('carrier_is_approved', models.BooleanField(default=False)),
                ('pick_up_time_range_start', models.DateTimeField()),
                ('pick_up_time_range_end', models.DateTimeField()),
                ('pick_up_tz', timezone_field.fields.TimeZoneField(default=b'US/Eastern')),
                ('pick_up_dock', models.CharField(help_text='if known', max_length=100, blank=True)),
                ('picked_up_at', models.DateTimeField(null=True, blank=True)),
                ('delivery_time_range_start', models.DateTimeField()),
                ('delivery_time_range_end', models.DateTimeField()),
                ('delivery_tz', timezone_field.fields.TimeZoneField(default=b'US/Eastern')),
                ('delivery_dock', models.CharField(help_text='if known', max_length=100, blank=True)),
                ('delivered_at', models.DateTimeField(null=True, blank=True)),
                ('hash_key', models.CharField(help_text=b'SHA 256 hash value to prevent duplicate entries', max_length=64, null=True, blank=True)),
                ('trip_distance_miles', models.DecimalField(help_text='Distance of trip (automatically calculated on model save)', null=True, max_digits=9, decimal_places=0, blank=True)),
                ('delivery_status', models.IntegerField(default=1, choices=[(1, b'Open'), (2, b'Pending Pickup'), (3, b'Pending Delivery'), (4, b'Delivered'), (5, b'Pending Approval')])),
                ('extra_details', models.TextField(null=True, blank=True)),
                ('carrier', models.ForeignKey(blank=True, to='shipments.Carrier', null=True)),
                ('receiver', models.ForeignKey(related_name='incoming_shipments', to='shipments.Location')),
                ('shipper', models.ForeignKey(related_name='outgoing_shipments', to='shipments.Location')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ShipmentTrackingPoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField()),
                ('coordinate', django.contrib.gis.db.models.fields.PointField(srid=4326, geography=True)),
                ('carrier', models.ForeignKey(related_name='associated_carrier', to='shipments.Carrier')),
                ('shipment', models.ForeignKey(to='shipments.Shipment')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Shipper',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('company', models.CharField(max_length=160)),
                ('email', models.EmailField(max_length=75)),
                ('phone', models.CharField(max_length=20)),
                ('is_scraper', models.BooleanField(default=False)),
                ('verified', models.BooleanField(default=False)),
                ('rejected', models.BooleanField(default=False)),
                ('user', models.OneToOneField(null=True, default=None, blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='shipment',
            name='shipper_owner',
            field=models.ForeignKey(related_name='Entity who created this shipment', to='shipments.Shipper'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='location',
            name='shipper',
            field=models.ForeignKey(related_name='associated_company', blank=True, to='shipments.Shipper', null=True),
            preserve_default=True,
        ),
    ]
