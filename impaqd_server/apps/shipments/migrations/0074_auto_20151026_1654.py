# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0073_auto_20151026_1651'),
    ]

    operations = [
        migrations.RenameField(
            model_name='genericuser',
            old_name='phone_2',
            new_name='phone',
        ),
        migrations.RenameField(
            model_name='person',
            old_name='phone_2',
            new_name='phone',
        ),
    ]
