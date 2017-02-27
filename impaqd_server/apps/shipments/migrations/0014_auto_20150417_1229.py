# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0013_auto_20150416_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filecontext',
            name='uuid_value',
            field=django_extensions.db.fields.UUIDField(editable=False, blank=True),
            preserve_default=True,
        ),
    ]
