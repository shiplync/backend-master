# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0096_auto_20160221_1112'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='savedlocation',
            options={'ordering': ('-updated_at',)},
        ),
    ]
