# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import impaqd_server.apps.geolocations.validators


class Migration(migrations.Migration):

    dependencies = [
        ('geolocations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geolocation',
            name='latitude',
            field=models.FloatField(editable=False, validators=[impaqd_server.apps.geolocations.validators.LatitudeValidator()]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='geolocation',
            name='longitude',
            field=models.FloatField(editable=False, validators=[impaqd_server.apps.geolocations.validators.LongitudeValidator()]),
            preserve_default=True,
        ),
    ]
