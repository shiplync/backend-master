# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0002_carrier_test_migrations_var'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carrier',
            name='test_migrations_var',
        ),
    ]
