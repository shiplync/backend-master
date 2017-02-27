# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geolocations', '0008_cachedcoordinate_cacheddistance'),
        ('shipments', '0093_remove_shipmentlocation_distance_to_next_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='savedlocation',
            name='cached_coordinate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='geolocations.CachedCoordinate', null=True),
        ),
    ]
