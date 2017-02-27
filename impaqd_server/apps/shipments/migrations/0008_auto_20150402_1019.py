# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0007_auto_20150401_1417'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipment',
            name='pallet_height',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='shipment',
            name='pallet_length',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='shipment',
            name='pallet_number',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='shipment',
            name='pallet_width',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='shipment',
            name='palletized',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='shipment',
            name='weight',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
