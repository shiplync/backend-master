# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def forward(apps, schema_editor):
    GenericUser = apps.get_model('shipments', 'GenericUser')
    Platform = apps.get_model('shipments', 'Platform')
    for u in GenericUser.objects.all():
        Platform.objects.create(
            user=u, platform_type=1, identifier=u.email, is_primary_email=True)
        if hasattr(u.user, 'carrier') and len(u.user.carrier.device_token) > 0:
            Platform.objects.create(
                user=u, platform_type=2,
                identifier=u.user.carrier.device_token)


def backward(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0032_shipment_carrier_company'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shipment',
            name='carrier',
        ),
        migrations.RenameField(
            model_name='shipment',
            old_name='carrier_company',
            new_name='carrier',
        ),
        migrations.RunPython(forward, backward),
    ]
