# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def forward(apps, schema_editor):
    CarrierDriver = apps.get_model('shipments', 'CarrierDriver')
    ShipperLogisticsManager = apps.get_model('shipments', 'ShipperLogisticsManager')
    GenericUser = apps.get_model('shipments', 'GenericUser')

    for c in CarrierDriver.objects.all():
    	g = GenericUser.objects.get(pk=c.genericuser_ptr_id)
        g.company2 = c.company
        g.save()

    for s in ShipperLogisticsManager.objects.all():
        g = GenericUser.objects.get(pk=s.genericuser_ptr_id)
        g.company2 = s.company
        g.save()

def backward(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0045_auto_20150902_1803'),
    ]

    operations = [
    	migrations.AddField(
            model_name='genericuser',
            name='company2',
            field=models.ForeignKey(blank=True, to='shipments.GenericCompany', null=True),
            preserve_default=True,
        ),
        migrations.RunPython(forward, backward),
    ]
