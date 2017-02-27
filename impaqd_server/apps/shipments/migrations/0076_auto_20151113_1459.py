# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0075_auto_20151026_1702'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='owner',
        ),
        migrations.AddField(
            model_name='location',
            name='features',
            field=models.OneToOneField(null=True, blank=True, to='shipments.ShipmentFeatures'),
        ),
        migrations.AddField(
            model_name='location',
            name='location_type',
            field=models.IntegerField(default=0, choices=[(0, b'Unknown'), (1, b'Pick up'), (2, b'Pick up and drop off'), (3, b'Drop off')]),
        ),
        migrations.AddField(
            model_name='location',
            name='shipment',
            field=models.ForeignKey(blank=True, to='shipments.Shipment', null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='time_range',
            field=models.OneToOneField(null=True, blank=True, to='shipments.TimeRange'),
        ),
        migrations.AddField(
            model_name='savedlocation',
            name='features',
            field=models.OneToOneField(null=True, blank=True, to='shipments.ShipmentFeatures'),
        ),
        migrations.AddField(
            model_name='savedlocation',
            name='location_type',
            field=models.IntegerField(default=0, choices=[(0, b'Unknown'), (1, b'Pick up'), (2, b'Pick up and drop off'), (3, b'Drop off')]),
        ),
        migrations.AddField(
            model_name='savedlocation',
            name='time_range',
            field=models.OneToOneField(null=True, blank=True, to='shipments.TimeRange'),
        ),
        migrations.AlterField(
            model_name='location',
            name='contact',
            field=models.OneToOneField(null=True, blank=True, to='shipments.Person'),
        ),
        migrations.AlterField(
            model_name='savedlocation',
            name='contact',
            field=models.OneToOneField(null=True, blank=True, to='shipments.Person'),
        ),
        migrations.AddField(
            model_name='location',
            name='arrival_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
