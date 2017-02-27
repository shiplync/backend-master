# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BasePermission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
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
                ('user_type', models.IntegerField(default=0, choices=[(0, b'Unknown'), (1, b'Shipper Manager'), (101, b'Carrier Manager'), (102, b'Carrier Driver'), (103, b'Carrier Dispatcher')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='basepermission',
            name='permission_collection',
            field=models.ForeignKey(related_name='permissions', to='permissions.BasePermissionCollection'),
            preserve_default=True,
        ),
    ]
