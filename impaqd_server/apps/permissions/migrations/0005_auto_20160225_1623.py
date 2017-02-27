# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permissions', '0004_auto_20160225_1623'),
    ]

    operations = [
    	migrations.RenameField(
            model_name='basepermissioncollection',
            old_name='user_type2',
            new_name='user_type',
        ),
    ]