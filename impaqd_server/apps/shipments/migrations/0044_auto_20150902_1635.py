# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0043_genericcompany_company_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrierdispatcher',
            name='company',
            field=models.ForeignKey(to='shipments.GenericCompany'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='carrierdriver',
            name='company',
            field=models.ForeignKey(to='shipments.GenericCompany'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demoaccount',
            name='carrier',
            field=models.ForeignKey(related_name='demoaccount_carrier', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='shipments.GenericCompany', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='demoaccount',
            name='shipper',
            field=models.ForeignKey(related_name='demoaccount_shipper', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='shipments.GenericCompany', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shipment',
            name='carrier',
            field=models.ForeignKey(related_name='active_shipments', blank=True, to='shipments.GenericCompany', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shipmentrequest',
            name='carrier',
            field=models.ForeignKey(to='shipments.GenericCompany'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shipperlogisticsmanager',
            name='company',
            field=models.ForeignKey(to='shipments.GenericCompany'),
            preserve_default=True,
        ),
    ]
