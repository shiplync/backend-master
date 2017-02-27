# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('permissions', '0001_initial'),
        ('shipments', '0052_auto_20150909_1845'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basepermission',
            name='permission',
        ),
        migrations.RemoveField(
            model_name='basepermission',
            name='permission_collection',
        ),
        migrations.DeleteModel(
            name='BasePermission',
        ),
        migrations.AlterField(
            model_name='genericuser',
            name='permissions',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='permissions.BasePermissionCollection'),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='BasePermissionCollection',
        ),
    ]
