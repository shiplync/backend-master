# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0059_companyinvite_invitee_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyinvite',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 8, 13, 38, 8, 576419, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='companyinvite',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 8, 13, 38, 19, 664361, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='companyrelation',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 8, 13, 38, 26, 352817, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='companyrelation',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 8, 13, 38, 35, 253957, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shipmentassignment',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 8, 13, 38, 43, 62533, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shipmentassignment',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 8, 13, 38, 50, 926586, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
