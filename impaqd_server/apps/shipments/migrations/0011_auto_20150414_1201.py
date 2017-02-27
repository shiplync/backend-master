# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0010_auto_20150410_1658'),
    ]

    operations = [                
        migrations.CreateModel(
            name='FileContext',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uuid_value', models.CharField(max_length=36)),
                ('path', models.CharField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ShipmentRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rejected', models.BooleanField(default=False)),
                ('carrier', models.ForeignKey(to='shipments.CarrierCompany')),
                ('driver', models.ForeignKey(blank=True, to='shipments.CarrierDriver', null=True)),
                ('shipment', models.ForeignKey(related_name='carrier_requests', to='shipments.Shipment')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='request',
            name='carrier',
        ),
        migrations.RemoveField(
            model_name='request',
            name='driver',
        ),
        migrations.RemoveField(
            model_name='request',
            name='shipment',
        ),
        migrations.DeleteModel(
            name='Request',
        ),
        migrations.AddField(
            model_name='genericuser',
            name='profile_photo',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='shipments.FileContext'),
            preserve_default=True,
        ),
    ]
