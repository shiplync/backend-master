# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0011_auto_20150414_1201'),
    ]

    operations = [
        migrations.CreateModel(
            name='TOSAcceptance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(null=True, default=None, blank=True, to='shipments.GenericUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
