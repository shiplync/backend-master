# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0088_auto_20151130_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipmenttag',
            name='tag_type',
            field=models.IntegerField(default=1, choices=[(1, b'Flatbed'), (2, b'Van'), (3, b'Reefer'), (4, b'Power Only'), (1001, b'Tarps'), (1003, b'Vented')]),
        ),
    ]
