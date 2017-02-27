# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0050_auto_20150909_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basepermission',
            name='permission_collection',
            field=models.ForeignKey(related_name='permissions', to='shipments.BasePermissionCollection'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='genericuser',
            name='permissions',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='shipments.BasePermissionCollection'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='genericuser',
            name='user_type',
            field=models.IntegerField(default=0, choices=[(0, b'Unknown'), (1, b'Shipper Manager'), (101, b'Carrier Manager'), (102, b'Carrier Driver'), (103, b'Carrier Dispatcher')]),
            preserve_default=True,
        ),
    ]
