# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0082_auto_20151117_1529'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='savedlocation',
            name='address',
        ),
        migrations.RemoveField(
            model_name='savedlocation',
            name='address_2',
        ),
        migrations.RemoveField(
            model_name='savedlocation',
            name='city',
        ),
        migrations.RemoveField(
            model_name='savedlocation',
            name='coordinate',
        ),
        migrations.RemoveField(
            model_name='savedlocation',
            name='state',
        ),
        migrations.RemoveField(
            model_name='savedlocation',
            name='zip_code',
        ),
        migrations.RemoveField(
            model_name='shipmentlocation',
            name='address',
        ),
        migrations.RemoveField(
            model_name='shipmentlocation',
            name='address_2',
        ),
        migrations.RemoveField(
            model_name='shipmentlocation',
            name='city',
        ),
        migrations.RemoveField(
            model_name='shipmentlocation',
            name='coordinate',
        ),
        migrations.RemoveField(
            model_name='shipmentlocation',
            name='state',
        ),
        migrations.RemoveField(
            model_name='shipmentlocation',
            name='zip_code',
        )
    ]
