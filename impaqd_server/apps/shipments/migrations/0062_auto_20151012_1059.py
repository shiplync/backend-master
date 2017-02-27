# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0061_auto_20151009_1625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demoaccount',
            name='connections',
            field=models.ManyToManyField(related_name='demo_account_companies', to='shipments.GenericCompany', blank=True),
        ),
    ]
