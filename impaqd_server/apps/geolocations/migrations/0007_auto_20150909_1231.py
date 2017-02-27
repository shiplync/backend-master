# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geolocations', '0006_auto_20150902_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geolocation',
            name='driver',
            field=models.ForeignKey(to='shipments.GenericUser', blank=True),
            preserve_default=True,
        ),
    ]
