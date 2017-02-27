# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0035_globalsettings_current_tos_version'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='platform',
            unique_together=set([('platform_type', 'identifier')]),
        ),
    ]
