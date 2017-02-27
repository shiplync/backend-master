# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
        ('shipments', '0115_auto_20160510_1344'),
    ]

    operations = [
        migrations.AddField(
            model_name='genericcompany',
            name='subscription',
            field=models.OneToOneField(null=True, blank=True, to='payments.Subscription'),
        ),
    ]
