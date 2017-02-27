# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def forward(apps, schema_editor):
    Shipment = apps.get_model('shipments', 'Shipment')
    for s in Shipment.objects.all():
        if (s.carrier and hasattr(s.carrier, 'user') and
                hasattr(s.carrier.user, 'genericuser') and
                hasattr(s.carrier.user.genericuser, 'carrierdriver')):
            s.carrier_company = \
                s.carrier.user.genericuser.carrierdriver.company
            s.save()


def backward(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0031_auto_20150619_1135'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipment',
            name='carrier_company',
            field=models.ForeignKey(related_name='active_shipments', blank=True, to='shipments.CarrierCompany', null=True),
            preserve_default=True,
        ),
        migrations.RunPython(forward, backward),
    ]
