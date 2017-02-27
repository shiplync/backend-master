# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0057_auto_20151002_1138'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='demoaccount',
            name='carrier',
        ),
        migrations.RemoveField(
            model_name='demoaccount',
            name='carrier_dot',
        ),
        migrations.RemoveField(
            model_name='demoaccount',
            name='carrier_email',
        ),
        migrations.RemoveField(
            model_name='demoaccount',
            name='shipper',
        ),
        migrations.RemoveField(
            model_name='demoaccount',
            name='shipper_email',
        ),
        migrations.AddField(
            model_name='demoaccount',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='shipments.GenericCompany', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='demoaccount',
            name='connections',
            field=models.ManyToManyField(related_name='demo_account_companies', null=True, to='shipments.GenericCompany', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='demoaccount',
            name='demo_account_type',
            field=models.IntegerField(default=1, choices=[(0, b'Unknown'), (1, b'Shipper'), (2, b'Carrier')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='demoaccount',
            name='dot',
            field=models.IntegerField(max_length=7, unique=True, null=True, verbose_name=b'DOT', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='demoaccount',
            name='no_of_connections',
            field=models.IntegerField(default=5),
            preserve_default=True,
        ),
    ]
