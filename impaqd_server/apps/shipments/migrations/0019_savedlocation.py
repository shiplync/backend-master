# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import impaqd_server.apps.shipments.validators
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0018_tosacceptance_shipper_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='SavedLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('location_name', models.CharField(max_length=100, null=True, blank=True)),
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
                ('shipper', models.ForeignKey(related_name='associated_shipper', blank=True, to='shipments.Shipper', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
