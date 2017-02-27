# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0014_auto_20150417_1229'),
    ]

    operations = [
        migrations.AddField(
            model_name='genericcompany',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 27, 21, 58, 34, 455703, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='genericcompany',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 27, 21, 58, 43, 5334, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='genericuser',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 27, 21, 58, 46, 504152, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='genericuser',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 27, 21, 58, 48, 743043, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
