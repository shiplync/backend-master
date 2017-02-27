# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='payment_ready',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='subscription',
            name='trial_length',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='subscription',
            name='trial_start',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
