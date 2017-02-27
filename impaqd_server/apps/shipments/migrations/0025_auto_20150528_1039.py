# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0024_auto_20150526_1859'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='hash_key',
        ),
        migrations.RemoveField(
            model_name='savedlocation',
            name='hash_key',
        ),
        migrations.RemoveField(
            model_name='shipment',
            name='hash_key',
        ),
    ]
