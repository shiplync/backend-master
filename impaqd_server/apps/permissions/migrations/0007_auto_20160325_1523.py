# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permissions', '0006_auto_20160323_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basepermissioncollection',
            name='user_type',
            field=models.CharField(default=b'unknown', max_length=200, choices=[(b'unknown', b'Unknown'), (b'brokermanager', b'Broker Manager'), (b'carriermanager', b'Carrier Manager'), (b'brokersupervisor', b'Broker Supervisor'), (b'carriersupervisor', b'Carrier Supervisor'), (b'brokerrepresentative', b'Broker Representative'), (b'carrierrepresentative', b'Carrier Representative'), (b'carrierdriver', b'Carrier Driver')]),
        ),
    ]
