# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0038_demoaccount'),
    ]

    operations = [
        migrations.AddField(
            model_name='genericcompany',
            name='dot1',
            field=models.IntegerField(max_length=7, unique=True, null=True, verbose_name=b'DOT1', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='genericcompany',
            name='is_fleet1',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='genericcompany',
            name='max_requests1',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
    ]
