# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0049_auto_20150909_1231'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CarrierOwnerPermissionCollection',
            new_name='CarrierManagerPermissionCollection',
        ),
        migrations.RenameModel(
            old_name='ShipperOwnerPermissionCollection',
            new_name='ShipperManagerPermissionCollection',
        ),
        migrations.RemoveField(
            model_name='logisticsmanagerpermissioncollection',
            name='basepermissioncollection_ptr',
        ),
        migrations.DeleteModel(
            name='LogisticsManagerPermissionCollection',
        ),
        migrations.AlterField(
            model_name='genericuser',
            name='user_type',
            field=models.IntegerField(default=0, choices=[(0, b'Unknown'), (1, b'Shipper Manager'), (101, b'Carrier Driver'), (102, b'Carrier Dispatcher')]),
            preserve_default=True,
        ),
    ]
