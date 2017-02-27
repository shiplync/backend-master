# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0094_savedlocation_cached_coordinate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='addressdetails',
            name='coordinate',
        ),
    ]
