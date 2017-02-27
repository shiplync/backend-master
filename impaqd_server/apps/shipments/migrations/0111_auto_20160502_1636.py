# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0110_auto_20160422_1126'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userinvite',
            options={'ordering': ('first_name',)},
        ),
    ]
