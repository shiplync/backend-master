# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0100_auto_20160225_1604'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipment',
            name='bol_number',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
