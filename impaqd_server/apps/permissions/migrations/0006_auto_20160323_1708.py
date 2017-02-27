# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permissions', '0005_auto_20160225_1623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basepermissioncollection',
            name='user_type',
            field=models.CharField(default=0, max_length=200, choices=[(0, b'Unknown'), (b'brokermanager', b'Broker Manager'), (b'carriermanager', b'Carrier Manager'), (b'brokersupervisor', b'Broker Supervisor'), (b'carriersupervisor', b'Carrier Supervisor'), (b'brokerrepresentative', b'Broker Representative'), (b'carrierrepresentative', b'Carrier Representative'), (b'carrierdriver', b'Carrier Driver')]),
        ),
    ]
