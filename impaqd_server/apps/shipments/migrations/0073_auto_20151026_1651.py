# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0072_auto_20151026_1639'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genericuser',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='person',
            name='phone',
        ),
    ]
