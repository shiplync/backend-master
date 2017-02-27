# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0089_auto_20151208_1410'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='equipmenttag',
            options={'ordering': ('tag_category',)},
        ),
        migrations.AlterModelOptions(
            name='shipment',
            options={'ordering': ('-pk',), 'permissions': (('view_shipment', 'View Shipment'),)},
        ),
        # migrations.AlterField(
        #     model_name='companyinvite',
        #     name='invitee_company_type',
        #     field=models.CharField(default=b'unknown', max_length=200, choices=[(b'unknown', b'Unknown'), (b'shipper', b'Shipper'), (b'carrier', b'Carrier')]),
        # ),
        # migrations.AlterField(
        #     model_name='demoaccount',
        #     name='demo_account_type',
        #     field=models.CharField(default=b'shipper', max_length=200, choices=[(b'unknown', b'Unknown'), (b'shipper', b'Shipper'), (b'carrier', b'Carrier')]),
        # ),
        migrations.AlterField(
            model_name='demoaccount',
            name='phone',
            field=models.CharField(default=b'+19125552222', max_length=20),
        ),
        # migrations.AlterField(
        #     model_name='genericcompany',
        #     name='company_type',
        #     field=models.CharField(default=b'unknown', max_length=200, choices=[(b'unknown', b'Unknown'), (b'shipper', b'Shipper'), (b'carrier', b'Carrier')]),
        # ),
        # migrations.AlterField(
        #     model_name='genericuser',
        #     name='user_type',
        #     field=models.CharField(default=b'unknown', max_length=200, choices=[(b'unknown', b'Unknown'), (b'shippermanager', b'Shipper Manager'), (b'carriermanager', b'Carrier Manager'), (b'carrierdriver', b'Carrier Driver'), (b'carrierdispatcher', b'Carrier Dispatcher')]),
        # ),
        migrations.AlterField(
            model_name='shipment',
            name='delivery_status',
            field=models.IntegerField(default=1, choices=[(1, b'Open'), (2, b'Pending Pickup'), (3, b'Enroute'), (4, b'Delivered'), (5, b'Pending Approval')]),
        ),
        ###
        migrations.AddField(
            model_name='companyinvite',
            name='invitee_company_type2',
            field=models.CharField(default=b'unknown', max_length=200, choices=[(b'unknown', b'Unknown'), (b'shipper', b'Shipper'), (b'carrier', b'Carrier')]),
        ),
        migrations.AddField(
            model_name='demoaccount',
            name='demo_account_type2',
            field=models.CharField(default=b'shipper', max_length=200, choices=[(b'unknown', b'Unknown'), (b'shipper', b'Shipper'), (b'carrier', b'Carrier')]),
        ),
        migrations.AddField(
            model_name='genericcompany',
            name='company_type2',
            field=models.CharField(default=b'unknown', max_length=200, choices=[(b'unknown', b'Unknown'), (b'shipper', b'Shipper'), (b'carrier', b'Carrier')]),
        ),
        migrations.AddField(
            model_name='genericuser',
            name='user_type2',
            field=models.CharField(default=b'unknown', max_length=200, choices=[(b'unknown', b'Unknown'), (b'shippermanager', b'Shipper Manager'), (b'carriermanager', b'Carrier Manager'), (b'carrierdriver', b'Carrier Driver'), (b'carrierdispatcher', b'Carrier Dispatcher')]),
        ),
    ]
