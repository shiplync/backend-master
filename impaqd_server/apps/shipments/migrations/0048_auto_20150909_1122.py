# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def forward(apps, schema_editor):
    GenericUser = apps.get_model('shipments', 'GenericUser')

    for g in GenericUser.objects.all():
        if hasattr(g, 'carrierdriver'):
            g.user_type = 101
        elif hasattr(g, 'shipperlogisticsmanager'):
            g.user_type = 1
        g.save()

def backward(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0047_auto_20150909_1115'),
    ]

    operations = [
        migrations.RenameField(
            model_name='genericuser',
            old_name='company2',
            new_name='company',
        ),
        migrations.AddField(
            model_name='genericuser',
            name='user_type',
            field=models.IntegerField(default=0, choices=[(0, b'Unknown'), (1, b'Shipper Logistics Manager'), (101, b'Carrier Driver'), (102, b'Carrier Dispatcher')]),
            preserve_default=True,
        ),
        migrations.RunPython(forward, backward),
    ]
