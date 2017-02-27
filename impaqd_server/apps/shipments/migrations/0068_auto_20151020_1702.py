# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0067_auto_20151020_1455'),
    ]

    operations = [
        migrations.RenameField(
            model_name='savedlocation',
            old_name='location_name',
            new_name='saved_location_name',
        ),
        migrations.RemoveField(
            model_name='location',
            name='location_name',
        ),
        migrations.AddField(
            model_name='location',
            name='company_name',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='savedlocation',
            name='company_name',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
