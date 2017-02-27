# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def forward(apps, schema_editor):
    GenericCompany = apps.get_model('shipments', 'GenericCompany')
    CarrierCompany = apps.get_model('shipments', 'CarrierCompany')
    ShipperCompany = apps.get_model('shipments', 'ShipperCompany')

    for c in CarrierCompany.objects.all():
        g = GenericCompany.objects.get(pk=c.genericcompany_ptr_id)
        g.company_type = 2        
        g.save()

    for s in ShipperCompany.objects.all():
        g = GenericCompany.objects.get(pk=s.genericcompany_ptr_id)
        g.company_type = 1       
        g.save()

def backward(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0042_auto_20150902_1031'),
    ]

    operations = [
        migrations.AddField(
            model_name='genericcompany',
            name='company_type',
            field=models.IntegerField(default=0, choices=[(0, b'Unknown'), (1, b'Shipper'), (2, b'Carrier')]),
            preserve_default=True,
        ),
        migrations.RunPython(forward, backward),
    ]
