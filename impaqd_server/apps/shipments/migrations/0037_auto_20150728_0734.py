# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0036_auto_20150625_1708'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='platform',
            unique_together=set([]),
        ),
    ]
