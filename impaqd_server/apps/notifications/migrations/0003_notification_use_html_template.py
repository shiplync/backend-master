# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_signupinternalnotif'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='use_html_template',
            field=models.BooleanField(default=True),
        ),
    ]
