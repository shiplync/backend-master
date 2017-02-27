# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0099_auto_20160225_1559'),
    ]

    operations = [
    	migrations.RenameField(
            model_name='genericuser',
            old_name='user_type2',
            new_name='user_type',
        ),
		migrations.RenameField(
            model_name='genericcompany',
            old_name='company_type2',
            new_name='company_type',
        ),
        migrations.RenameField(
            model_name='companyinvite',
            old_name='invitee_company_type2',
            new_name='invitee_company_type',
        ),
        migrations.RenameField(
            model_name='demoaccount',
            old_name='demo_account_type2',
            new_name='demo_account_type',
        ),
    ]
