# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geolocations', '0003_auto_20150622_1247'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='geolocation',
            unique_together=set([('carrier', 'driver', 'timestamp')]),
        ),
    ]
