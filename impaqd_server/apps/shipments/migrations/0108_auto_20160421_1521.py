# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0107_auto_20160407_1057'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='companydivision',
            options={'ordering': ('name',)},
        ),
        migrations.AddField(
            model_name='genericuser',
            name='inactive',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='companydivision',
            name='name',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userinvite',
            name='first_name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
