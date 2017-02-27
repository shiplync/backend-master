# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def forward(apps, schema_editor):
    BasePermissionCollection = apps.get_model('permissions', 'BasePermissionCollection')

    for o in BasePermissionCollection.objects.all():
    	if o.user_type == 1:
    		o.user_type2 = 'shippermanager'
    	else:
    		o.user_type2 = 'carriermanager'
        o.save()


def backward(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('permissions', '0002_auto_20160128_1156'),
    ]

    operations = [
    	migrations.RunPython(forward, backward),
    ]
