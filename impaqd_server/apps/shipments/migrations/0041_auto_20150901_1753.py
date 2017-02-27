# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0040_auto_20150901_1746'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carriercompany',
            name='dot',
        ),
        migrations.RemoveField(
            model_name='carriercompany',
            name='is_fleet',
        ),
        migrations.RemoveField(
            model_name='carriercompany',
            name='max_requests',
        ),
        migrations.RenameField(
            model_name='genericcompany',
            old_name='is_fleet1',
            new_name='is_fleet',
        ),
        migrations.RenameField(
            model_name='genericcompany',
            old_name='dot1',
            new_name='dot',
        ),
        migrations.RenameField(
            model_name='genericcompany',
            old_name='max_requests1',
            new_name='max_requests',
        ),        
    ]
