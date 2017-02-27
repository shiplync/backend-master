# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def forward(apps, schema_editor):
    GenericCompany = apps.get_model('shipments', 'GenericCompany')
    CarrierCompany = apps.get_model('shipments', 'CarrierCompany')

    for c in CarrierCompany.objects.all():
    	g = GenericCompany.objects.get(pk=c.genericcompany_ptr_id)
    	g.dot1 = c.dot
    	g.is_fleet1 = c.is_fleet
    	g.max_requests1 = c.max_requests
    	g.save()

def backward(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0039_auto_20150901_1744'),
    ]

    operations = [
    	migrations.RunPython(forward, backward),
    ]
