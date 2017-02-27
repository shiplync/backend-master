# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0068_auto_20151020_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='coordinate',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, geography=True, blank=True),
        ),
        migrations.AlterField(
            model_name='savedlocation',
            name='coordinate',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, geography=True, blank=True),
        ),
    ]
