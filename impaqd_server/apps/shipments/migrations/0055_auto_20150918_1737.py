# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0054_auto_20150915_1710'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='companyrelation',
            unique_together=set([('relation_from', 'relation_to')]),
        ),
    ]
