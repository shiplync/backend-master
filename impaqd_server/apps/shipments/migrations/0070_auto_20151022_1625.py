# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0069_auto_20151022_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='address',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='savedlocation',
            name='address',
            field=models.TextField(null=True, blank=True),
        ),
    ]
