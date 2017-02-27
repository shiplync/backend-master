# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.db import transaction

def forward(apps, schema_editor):
    pass
#    from impaqd_server.apps.shipments.models import Shipper, Shipment, TOSAcceptance
#
#    # Create ShipperCompany and ShipperLogisticsManager
#    shippers = Shipper.objects.all()
#    for s in shippers:
#        s.save()
#
#    # Set owner on all shipment objects
#    shipments = Shipment.objects.all()
#    for s in shipments:
#        s.save()
#
#    # Set TOS Acceptance
#    tos = TOSAcceptance.objects.all()
#    for t in tos:
#        t.save()

def backward(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0023_auto_20150526_1454'),
    ]
    operations = [
        migrations.RunPython(forward, backward),
    ]
