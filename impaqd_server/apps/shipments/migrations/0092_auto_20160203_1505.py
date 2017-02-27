# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geolocations', '0008_cachedcoordinate_cacheddistance'),
        ('shipments', '0091_auto_20160201_1644'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipmentlocation',
            name='cached_coordinate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='geolocations.CachedCoordinate', null=True),
        ),
        migrations.AddField(
            model_name='shipmentlocation',
            name='cached_distance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='geolocations.CachedDistance', null=True),
        ),
    ]
