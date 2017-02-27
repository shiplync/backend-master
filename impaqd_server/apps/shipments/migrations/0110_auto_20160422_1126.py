# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0109_auto_20160421_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demoaccount',
            name='password',
            field=models.CharField(default=b'flatbed', max_length=100),
        ),
    ]
