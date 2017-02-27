# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permissions', '0001_initial'),
    ]

    operations = [
        # migrations.AlterField(
        #     model_name='basepermissioncollection',
        #     name='user_type',
        #     field=models.CharField(default=b'unknown', max_length=200, choices=[(b'unknown', b'Unknown'), (b'shippermanager', b'Shipper Manager'), (b'carriermanager', b'Carrier Manager'), (b'carrierdriver', b'Carrier Driver'), (b'carrierdispatcher', b'Carrier Dispatcher')]),
        # ),
        migrations.AddField(
            model_name='basepermissioncollection',
            name='user_type2',
            field=models.CharField(default=b'unknown', max_length=200, choices=[(b'unknown', b'Unknown'), (b'shippermanager', b'Shipper Manager'), (b'carriermanager', b'Carrier Manager'), (b'carrierdriver', b'Carrier Driver'), (b'carrierdispatcher', b'Carrier Dispatcher')]),
        ),
    ]
