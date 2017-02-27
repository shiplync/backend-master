# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0070_auto_20151022_1625'),
    ]

    operations = [
        migrations.AddField(
            model_name='genericuser',
            name='phone_2',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='phone_2',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, blank=True, null=True),
        ),
    ]
