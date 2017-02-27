# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0030_remove_tosacceptance_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('platform_type', models.IntegerField(choices=[(1, b'Email'), (2, b'iOS'), (3, b'Android')])),
                ('identifier', models.CharField(default=b'', help_text=b'UDID, email etc.', max_length=512)),
                ('allow_notifications', models.BooleanField(default=True)),
                ('user', models.ForeignKey(to='shipments.GenericUser')),
                ('is_primary_email', models.BooleanField(default=False, help_text=b'In sync with the users email. Only one platform needs to have this field set to True')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='device',
            name='user',
        ),
        migrations.DeleteModel(
            name='Device',
        ),
    ]
