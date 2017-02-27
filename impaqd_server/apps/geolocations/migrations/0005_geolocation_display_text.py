# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geolocations', '0004_auto_20150623_1012'),
    ]

    operations = [
        migrations.AddField(
            model_name='geolocation',
            name='display_text',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
