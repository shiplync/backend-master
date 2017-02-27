# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0033_auto_20150618_1250'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carrier',
            name='user',
        ),
        migrations.RemoveField(
            model_name='shipmenttrackingpoint',
            name='carrier',
        ),
        migrations.DeleteModel(
            name='Carrier',
        ),
        migrations.RemoveField(
            model_name='shipmenttrackingpoint',
            name='shipment',
        ),
        migrations.DeleteModel(
            name='ShipmentTrackingPoint',
        ),
    ]
