# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0017_filecontext_url_ttl'),
    ]

    operations = [
        migrations.AddField(
            model_name='tosacceptance',
            name='shipper_user',
            field=models.OneToOneField(null=True, default=None, blank=True, to='shipments.Shipper'),
            preserve_default=True,
        ),
    ]
