# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0114_auto_20160510_1152'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='shipmentassignment',
            unique_together=set([]),
        ),
    ]
