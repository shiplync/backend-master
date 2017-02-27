# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shipments', '0005_location_location_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('platform', models.IntegerField(default=1, null=True, blank=True, choices=[(1, b'Unknown'), (2, b'iOS'), (3, b'Android'), (4, b'Web')])),
                ('identifier', models.CharField(default=b'', max_length=512, null=True, help_text=b'UDID or similar', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GenericCompany',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company_name', models.CharField(max_length=200)),
                ('verified', models.BooleanField(default=False)),
                ('rejected', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CarrierCompany',
            fields=[
                ('genericcompany_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='shipments.GenericCompany')),
                ('dot', models.IntegerField(unique=True, max_length=7, verbose_name=b'DOT')),
                ('mc', models.CharField(max_length=32, null=True, verbose_name=b'MC', blank=True)),
                ('is_fleet', models.BooleanField(default=False)),
                ('max_requests', models.IntegerField(default=1)),
            ],
            options={
            },
            bases=('shipments.genericcompany',),
        ),
        migrations.CreateModel(
            name='GenericUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(unique=True, max_length=75)),
                ('first_name', models.CharField(max_length=100, null=True, blank=True)),
                ('last_name', models.CharField(max_length=100, null=True, blank=True)),
                ('phone', models.CharField(max_length=20, null=True, blank=True)),
                ('photo', models.TextField(help_text=b'Photo (encoded as a base64 string)', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CarrierDriver',
            fields=[
                ('genericuser_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='shipments.GenericUser')),
                ('last_location', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, geography=True, blank=True)),
                ('last_location_timestamp', models.DateTimeField(null=True, blank=True)),
                ('vehicle_type', models.IntegerField(default=1, null=True, blank=True, choices=[(1, b'Flatbed'), (2, b'Reefer'), (3, b'Van'), (4, b'Power only')])),
                ('company', models.ForeignKey(related_name='belonging_drivers', to='shipments.CarrierCompany')),
            ],
            options={
            },
            bases=('shipments.genericuser',),
        ),
        migrations.CreateModel(
            name='CarrierDispatcher',
            fields=[
                ('genericuser_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='shipments.GenericUser')),
                ('company', models.ForeignKey(related_name='belonging_dispatchers', to='shipments.CarrierCompany')),
            ],
            options={
            },
            bases=('shipments.genericuser',),
        ),
        migrations.CreateModel(
            name='Insurance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('policy_url', models.CharField(max_length=2048, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('approved', models.BooleanField(default=False)),
                ('carrier', models.ForeignKey(to='shipments.CarrierCompany')),
                ('driver', models.ForeignKey(blank=True, to='shipments.CarrierDriver', null=True)),
                ('shipment', models.ForeignKey(related_name='carrier_requests', to='shipments.Shipment')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='genericuser',
            name='user',
            field=models.OneToOneField(null=True, default=None, blank=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='genericcompany',
            name='insurance',
            field=models.OneToOneField(related_name='company_insurance', null=True, blank=True, to='shipments.Insurance'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='genericcompany',
            name='owner',
            field=models.ForeignKey(blank=True, to='shipments.GenericUser', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='device',
            name='user',
            field=models.ForeignKey(related_name='belonging_users', to='shipments.GenericUser'),
            preserve_default=True,
        ),
    ]
