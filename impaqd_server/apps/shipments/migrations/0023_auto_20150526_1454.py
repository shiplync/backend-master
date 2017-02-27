# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import transaction
from django.db import models, migrations

class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0022_auto_20150522_1228'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarrierOwnerPermissionCollection',
            fields=[
                ('basepermissioncollection_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='shipments.BasePermissionCollection')),
            ],
            options={
            },
            bases=('shipments.basepermissioncollection',),
        ),
        migrations.CreateModel(
            name='LogisticsManagerPermissionCollection',
            fields=[
                ('basepermissioncollection_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='shipments.BasePermissionCollection')),
            ],
            options={
            },
            bases=('shipments.basepermissioncollection',),
        ),
        migrations.CreateModel(
            name='ShipperCompany',
            fields=[
                ('genericcompany_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='shipments.GenericCompany')),
            ],
            options={
            },
            bases=('shipments.genericcompany',),
        ),
        migrations.CreateModel(
            name='ShipperLogisticsManager',
            fields=[
                ('genericuser_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='shipments.GenericUser')),
                ('company', models.ForeignKey(to='shipments.ShipperCompany')),
            ],
            options={
            },
            bases=('shipments.genericuser',),
        ),
        migrations.CreateModel(
            name='ShipperOwnerPermissionCollection',
            fields=[
                ('basepermissioncollection_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='shipments.BasePermissionCollection')),
            ],
            options={
            },
            bases=('shipments.basepermissioncollection',),
        ),
        migrations.RemoveField(
            model_name='owneroperatorpermissioncollection',
            name='basepermissioncollection_ptr',
        ),
        migrations.DeleteModel(
            name='OwnerOperatorPermissionCollection',
        ),
        migrations.RemoveField(
            model_name='carriercompany',
            name='mc',
        ),
        migrations.AlterField(
            model_name='basepermission',
            name='name',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='carrierdispatcher',
            name='company',
            field=models.ForeignKey(to='shipments.CarrierCompany'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='carrierdriver',
            name='company',
            field=models.ForeignKey(to='shipments.CarrierCompany'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='device',
            name='user',
            field=models.ForeignKey(to='shipments.GenericUser'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shipmentrequest',
            name='shipment',
            field=models.ForeignKey(to='shipments.Shipment'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='shipment',
            name='owner',
            field=models.ForeignKey(default=None, blank=True, to='shipments.GenericCompany', null=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='shipment',
            name='shipper_owner',
            field=models.ForeignKey(blank=True, to='shipments.Shipper', help_text=b'Deprecated (Old shipper model). Use owner instead', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='location',
            name='owner',
            field=models.ForeignKey(blank=True, to='shipments.GenericCompany', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='savedlocation',
            name='owner',
            field=models.ForeignKey(blank=True, to='shipments.GenericCompany', null=True),
            preserve_default=True,
        ),
    ]

