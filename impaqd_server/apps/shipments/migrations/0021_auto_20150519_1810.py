# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('shipments', '0020_responsestatus'),
    ]

    operations = [
        migrations.CreateModel(
            name='BasePermission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('is_set', models.BooleanField(default=False)),
                ('is_editable', models.BooleanField(default=False)),
                ('permission', models.ForeignKey(to='auth.Permission')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BasePermissionCollection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DispatcherPermissionCollection',
            fields=[
                ('basepermissioncollection_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='shipments.BasePermissionCollection')),
            ],
            options={
            },
            bases=('shipments.basepermissioncollection',),
        ),
        migrations.CreateModel(
            name='DriverPermissionCollection',
            fields=[
                ('basepermissioncollection_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='shipments.BasePermissionCollection')),
            ],
            options={
            },
            bases=('shipments.basepermissioncollection',),
        ),
        migrations.CreateModel(
            name='OwnerOperatorPermissionCollection',
            fields=[
                ('basepermissioncollection_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='shipments.BasePermissionCollection')),
            ],
            options={
            },
            bases=('shipments.basepermissioncollection',),
        ),
        migrations.AddField(
            model_name='basepermission',
            name='permission_collection',
            field=models.ForeignKey(related_name='permissions', to='shipments.BasePermissionCollection'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='genericuser',
            name='permissions',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='shipments.BasePermissionCollection'),
            preserve_default=True,
        ),
    ]
