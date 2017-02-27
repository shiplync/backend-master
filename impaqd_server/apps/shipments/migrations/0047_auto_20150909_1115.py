# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0046_auto_20150909_1100'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carrierdispatcher',
            name='company',
        ),
        migrations.RemoveField(
            model_name='carrierdriver',
            name='company',
        ),
        migrations.RemoveField(
            model_name='shipperlogisticsmanager',
            name='company',
        ),
        migrations.AlterField(
            model_name='genericuser',
            name='company2',
            field=models.ForeignKey(to='shipments.GenericCompany'),
            preserve_default=True,
        ),
    ]
