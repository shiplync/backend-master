# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def forward(apps, schema_editor):
    GenericCompany = apps.get_model('shipments', 'GenericCompany')
    GenericUser = apps.get_model('shipments', 'GenericUser')
    CompanyInvite = apps.get_model('shipments', 'CompanyInvite')
    DemoAccount = apps.get_model('shipments', 'DemoAccount')

    for o in GenericUser.objects.all():
        if o.user_type == 1:
        	o.user_type2 = 'shippermanager'
        else:
        	o.user_type2 = 'carriermanager'
        o.save()
    for o in GenericCompany.objects.all():
        if o.company_type == 1:
        	o.company_type2 = 'shipper'
        else:
        	o.company_type2 = 'carrier'
        o.save()
    for o in CompanyInvite.objects.all():
        if o.invitee_company_type == 1:
        	o.invitee_company_type2 = 'shipper'
        else:
        	o.invitee_company_type2 = 'carrier'
        o.save()
    for o in DemoAccount.objects.all():
        if o.demo_account_type == 1:
        	o.demo_account_type2 = 'shipper'
        else:
        	o.demo_account_type2 = 'carrier'
        o.save()


def backward(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0097_auto_20160224_2150'),
    ]

    operations = [
    	migrations.RunPython(forward, backward),
    ]
