# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0116_genericcompany_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='genericcompany',
            name='registration_complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='genericcompany',
            name='verified',
            field=models.BooleanField(default=True),
        ),
    ]
