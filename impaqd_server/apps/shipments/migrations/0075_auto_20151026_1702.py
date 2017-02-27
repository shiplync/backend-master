# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0074_auto_20151026_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='appointment_id',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='location',
            name='comments',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='savedlocation',
            name='appointment_id',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='savedlocation',
            name='comments',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='shipment',
            name='comments',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='shipmentfeatures',
            name='comments',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='shipmentpayout',
            name='comments',
            field=models.TextField(null=True, blank=True),
        ),
    ]
