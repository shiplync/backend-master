# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0095_remove_addressdetails_coordinate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genericuser',
            name='photo',
        ),
        migrations.AddField(
            model_name='genericcompany',
            name='logo',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='shipments.FileContext'),
        ),
    ]
