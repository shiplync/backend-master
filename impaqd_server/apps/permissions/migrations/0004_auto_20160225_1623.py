# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permissions', '0003_auto_20160225_1613'),
    ]

    operations = [
    	migrations.RemoveField(
            model_name='basepermissioncollection',
            name='user_type',
        ),
    ]
