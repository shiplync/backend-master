# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0098_auto_20160225_1524'),
    ]

    operations = [
    	migrations.RemoveField(
            model_name='genericuser',
            name='user_type',
        ),
        migrations.RemoveField(
            model_name='genericcompany',
            name='company_type',
        ),
        migrations.RemoveField(
            model_name='companyinvite',
            name='invitee_company_type',
        ),
        migrations.RemoveField(
            model_name='demoaccount',
            name='demo_account_type',
        ),
    ]
