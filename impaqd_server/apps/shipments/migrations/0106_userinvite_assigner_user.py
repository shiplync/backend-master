# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0105_auto_20160325_1523'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinvite',
            name='assigner_user',
            field=models.ForeignKey(related_name='invited_users', blank=True, to='shipments.GenericUser', null=True),
        ),
    ]
