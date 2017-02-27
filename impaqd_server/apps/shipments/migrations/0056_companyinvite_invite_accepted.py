# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0055_auto_20150918_1737'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyinvite',
            name='invite_accepted',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
