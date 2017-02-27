# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0110_auto_20160422_1126'),
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SignupInternalNotif',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company', models.ForeignKey(to='shipments.GenericCompany')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
