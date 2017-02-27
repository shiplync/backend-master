# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_notification_use_html_template'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='email_sent',
            field=models.BooleanField(default=False),
        ),
    ]
