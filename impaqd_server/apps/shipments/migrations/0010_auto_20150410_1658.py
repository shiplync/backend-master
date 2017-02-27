# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0009_shipper_tos'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shipper',
            old_name='tos',
            new_name='tos_agreement_at',
        ),
    ]
