# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0051_auto_20150909_1733'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carriermanagerpermissioncollection',
            name='basepermissioncollection_ptr',
        ),
        migrations.DeleteModel(
            name='CarrierManagerPermissionCollection',
        ),
        migrations.RemoveField(
            model_name='dispatcherpermissioncollection',
            name='basepermissioncollection_ptr',
        ),
        migrations.DeleteModel(
            name='DispatcherPermissionCollection',
        ),
        migrations.RemoveField(
            model_name='driverpermissioncollection',
            name='basepermissioncollection_ptr',
        ),
        migrations.DeleteModel(
            name='DriverPermissionCollection',
        ),
        migrations.RemoveField(
            model_name='shippermanagerpermissioncollection',
            name='basepermissioncollection_ptr',
        ),
        migrations.DeleteModel(
            name='ShipperManagerPermissionCollection',
        ),
        migrations.AddField(
            model_name='basepermissioncollection',
            name='user_type',
            field=models.IntegerField(default=0, choices=[(0, b'Unknown'), (1, b'Shipper Manager'), (101, b'Carrier Manager'), (102, b'Carrier Driver'), (103, b'Carrier Dispatcher')]),
            preserve_default=True,
        ),
    ]
