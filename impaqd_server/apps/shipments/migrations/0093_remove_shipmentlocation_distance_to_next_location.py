# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0092_auto_20160203_1505'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shipmentlocation',
            name='distance_to_next_location',
        ),
    ]
