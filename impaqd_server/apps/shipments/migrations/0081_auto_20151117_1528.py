# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import impaqd_server.apps.shipments.validators
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0080_auto_20151116_1822'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddressDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.TextField(null=True, blank=True)),
                ('address_2', models.TextField(null=True, blank=True)),
                ('zip_code', models.CharField(blank=True, max_length=5, null=True, validators=[impaqd_server.apps.shipments.validators.validate_zip_code])),
                ('city', models.CharField(max_length=50, null=True, blank=True)),
                ('state', models.CharField(blank=True, max_length=2, null=True, choices=[(b'AL', b'ALABAMA'), (b'AK', b'ALASKA'), (b'AZ', b'ARIZONA'), (b'AR', b'ARKANSAS'), (b'CA', b'CALIFORNIA'), (b'CO', b'COLORADO'), (b'CT', b'CONNECTICUT'), (b'DE', b'DELAWARE'), (b'FL', b'FLORIDA'), (b'GA', b'GEORGIA'), (b'HI', b'HAWAII'), (b'ID', b'IDAHO'), (b'IL', b'ILLINOIS'), (b'IN', b'INDIANA'), (b'IA', b'IOWA'), (b'KS', b'KANSAS'), (b'KY', b'KENTUCKY'), (b'LA', b'LOUISIANA'), (b'ME', b'MAINE'), (b'MD', b'MARYLAND'), (b'MA', b'MASSACHUSETTS'), (b'MI', b'MICHIGAN'), (b'MN', b'MINNESOTA'), (b'MS', b'MISSISSIPPI'), (b'MO', b'MISSOURI'), (b'MT', b'MONTANA'), (b'NE', b'NEBRASKA'), (b'NV', b'NEVADA'), (b'NH', b'NEW HAMPSHIRE'), (b'NJ', b'NEW JERSEY'), (b'NM', b'NEW MEXICO'), (b'NY', b'NEW YORK'), (b'NC', b'NORTH CAROLINA'), (b'ND', b'NORTH DAKOTA'), (b'OH', b'OHIO'), (b'OK', b'OKLAHOMA'), (b'OR', b'OREGON'), (b'PA', b'PENNSYLVANIA'), (b'RI', b'RHODE ISLAND'), (b'SC', b'SOUTH CAROLINA'), (b'SD', b'SOUTH DAKOTA'), (b'TN', b'TENNESSEE'), (b'TX', b'TEXAS'), (b'UT', b'UTAH'), (b'VT', b'VERMONT'), (b'VA', b'VIRGINIA'), (b'WA', b'WASHINGTON'), (b'WV', b'WEST VIRGINIA'), (b'WI', b'WISCONSIN'), (b'WY', b'WYOMING')])),
                ('coordinate', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, geography=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='savedlocation',
            name='address_details',
            field=models.OneToOneField(null=True, blank=True, to='shipments.AddressDetails'),
        ),
        migrations.AddField(
            model_name='shipmentlocation',
            name='address_details',
            field=models.OneToOneField(null=True, blank=True, to='shipments.AddressDetails'),
        ),
    ]
