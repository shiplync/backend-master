# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0079_auto_20151114_1216'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shipmentlocation',
            options={'ordering': ('location_type', 'time_range__time_range_end')},
        ),
    ]
