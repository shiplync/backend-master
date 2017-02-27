# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('no_users', models.IntegerField(default=1, null=True, blank=True)),
                ('no_trucks', models.IntegerField(default=0, null=True, blank=True)),
                ('annual_plan', models.BooleanField(default=True)),
            ],
        ),
    ]
