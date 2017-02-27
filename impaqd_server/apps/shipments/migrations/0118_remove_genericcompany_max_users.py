# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0117_auto_20160609_0954'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genericcompany',
            name='max_users',
        ),
    ]
