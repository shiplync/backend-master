# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0037_auto_20150728_0734'),
    ]

    operations = [
        migrations.CreateModel(
            name='DemoAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(unique=True, max_length=75)),
                ('carrier_email', models.EmailField(unique=True, max_length=75)),
                ('shipper_email', models.EmailField(unique=True, max_length=75)),
                ('password', models.CharField(default=b'1234', max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('phone', models.CharField(default=b'5555555555', max_length=20)),
                ('company_name', models.CharField(max_length=200)),
                ('carrier_dot', models.IntegerField(unique=True, max_length=7, verbose_name=b'DOT')),
                ('no_of_shipments', models.IntegerField(default=40)),
                ('carrier', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='shipments.CarrierCompany', null=True)),
                ('shipper', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='shipments.ShipperCompany', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
