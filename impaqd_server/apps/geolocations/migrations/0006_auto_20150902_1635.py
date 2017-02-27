# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geolocations', '0005_geolocation_display_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geolocation',
            name='carrier',
            field=models.ForeignKey(to='shipments.GenericCompany', blank=True),
            preserve_default=True,
        ),
    ]
