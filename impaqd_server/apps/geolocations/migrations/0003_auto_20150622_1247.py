# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import impaqd_server.apps.geolocations.validators


class Migration(migrations.Migration):

    dependencies = [
        ('geolocations', '0002_auto_20150601_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geolocation',
            name='accuracy',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='geolocation',
            name='altitude',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='geolocation',
            name='carrier',
            field=models.ForeignKey(to='shipments.CarrierCompany', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='geolocation',
            name='course',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='geolocation',
            name='driver',
            field=models.ForeignKey(to='shipments.CarrierDriver', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='geolocation',
            name='latitude',
            field=models.FloatField(validators=[impaqd_server.apps.geolocations.validators.LatitudeValidator()]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='geolocation',
            name='longitude',
            field=models.FloatField(validators=[impaqd_server.apps.geolocations.validators.LongitudeValidator()]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='geolocation',
            name='shipment',
            field=models.ForeignKey(blank=True, to='shipments.Shipment', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='geolocation',
            name='speed',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='geolocation',
            name='timestamp',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
