# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import impaqd_server.apps.geolocations.validators


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0019_savedlocation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Geolocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('latitude', models.FloatField(editable=False, validators=[impaqd_server.apps.geolocations.validators.LatitudeValidator()])),
                ('longitude', models.FloatField(editable=False, validators=[impaqd_server.apps.geolocations.validators.LongitudeValidator()])),
                ('altitude', models.FloatField(null=True, editable=False, blank=True)),
                ('accuracy', models.FloatField(null=True, editable=False, blank=True)),
                ('speed', models.FloatField(null=True, editable=False, blank=True)),
                ('course', models.FloatField(null=True, editable=False, blank=True)),
                ('timestamp', models.DateTimeField(null=True, editable=False, blank=True)),
                ('carrier', models.ForeignKey(blank=True, editable=False, to='shipments.CarrierCompany')),
                ('driver', models.ForeignKey(blank=True, editable=False, to='shipments.CarrierDriver')),
                ('shipment', models.ForeignKey(blank=True, editable=False, to='shipments.Shipment', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
