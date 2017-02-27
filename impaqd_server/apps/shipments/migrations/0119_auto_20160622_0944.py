# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0118_remove_genericcompany_max_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demoaccount',
            name='demo_account_type',
            field=models.CharField(default=b'carrier', max_length=200, choices=[(b'unknown', b'Unknown'), (b'shipper', b'Shipper'), (b'carrier', b'Carrier')]),
        ),
    ]
