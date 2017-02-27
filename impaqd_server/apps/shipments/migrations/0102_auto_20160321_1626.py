# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0101_shipment_bol_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInvite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('token', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('email', models.EmailField(unique=True, max_length=254)),
                ('user_type', models.CharField(default=b'unknown', max_length=200, choices=[(b'unknown', b'Unknown'), (b'shippermanager', b'Shipper Manager'), (b'carriermanager', b'Carrier Manager'), (b'carrierdriver', b'Carrier Driver'), (b'carrierdispatcher', b'Carrier Dispatcher')])),
                ('first_name', models.CharField(max_length=100, null=True, blank=True)),
                ('last_name', models.CharField(max_length=100, null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='genericcompany',
            name='max_users',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='userinvite',
            name='company',
            field=models.ForeignKey(to='shipments.GenericCompany'),
        ),
        migrations.AddField(
            model_name='userinvite',
            name='user',
            field=models.OneToOneField(null=True, default=None, blank=True, to='shipments.GenericUser'),
        ),
    ]
