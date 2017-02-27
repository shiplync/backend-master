# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_auto_20160613_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='no_trucks',
            field=models.IntegerField(default=10, null=True, blank=True),
        ),
    ]
