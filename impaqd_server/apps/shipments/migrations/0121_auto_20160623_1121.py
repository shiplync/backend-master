# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0120_auto_20160622_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genericuser',
            name='user_type',
            field=models.CharField(default=b'unknown', max_length=200, choices=[(b'unknown', b'Unknown'), (b'brokermanager', b'Broker Manager'), (b'carriermanager', b'Admin'), (b'brokersupervisor', b'Broker Supervisor'), (b'carriersupervisor', b'Dispatcher'), (b'brokerrepresentative', b'Broker Representative'), (b'carrierdriver', b'Driver')]),
        ),
        migrations.AlterField(
            model_name='userinvite',
            name='user_type',
            field=models.CharField(default=b'unknown', max_length=200, choices=[(b'unknown', b'Unknown'), (b'brokermanager', b'Broker Manager'), (b'carriermanager', b'Admin'), (b'brokersupervisor', b'Broker Supervisor'), (b'carriersupervisor', b'Dispatcher'), (b'brokerrepresentative', b'Broker Representative'), (b'carrierdriver', b'Driver')]),
        ),
    ]
