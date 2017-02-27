# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import impaqd_server.apps.shipments.validators
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0076_auto_20151113_1459'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Location',
            new_name='ShipmentLocation',
        )
    ]
