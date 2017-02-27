# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0012_tosacceptance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipper',
            name='email',
            field=models.EmailField(unique=True, max_length=75),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shipper',
            name='tos_agreement_at',
            field=models.DateTimeField(default=None, null=True, blank=True),
            preserve_default=True,
        ),
    ]
