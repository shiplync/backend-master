# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0041_auto_20150901_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genericcompany',
            name='dot',
            field=models.IntegerField(max_length=10, unique=True, null=True, verbose_name=b'DOT', blank=True),
            preserve_default=True,
        ),
    ]
