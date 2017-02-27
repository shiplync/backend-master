# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def forward(apps, schema_editor):
    GenericUser = apps.get_model('shipments', 'GenericUser')
    BasePermissionCollection = apps.get_model('permissions', 'BasePermissionCollection')

    for o in GenericUser.objects.all():
        if o.company.company_type == 'carrier':
        	o.user_type = 'carriermanager'
        else:
            o.user_type = 'brokermanager'
        o.save()

    for o in BasePermissionCollection.objects.all():
        if o.genericuser.company.company_type == 'carrier':
            o.user_type = 'carriermanager'
        else:
            o.user_type = 'brokermanager'
        o.save()


def backward(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0108_auto_20160421_1521'),
    ]

    operations = [
    	migrations.RunPython(forward, backward),
    ]
