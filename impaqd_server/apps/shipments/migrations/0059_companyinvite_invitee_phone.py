# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0058_auto_20151006_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyinvite',
            name='invitee_phone',
            field=models.CharField(max_length=20, null=True, blank=True),
            preserve_default=True,
        ),
    ]
