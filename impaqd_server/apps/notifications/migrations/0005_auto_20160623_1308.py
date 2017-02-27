# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0121_auto_20160623_1121'),
        ('notifications', '0004_notification_email_sent'),
    ]

    operations = [
        migrations.CreateModel(
            name='Day1',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('receiver', models.OneToOneField(to='shipments.GenericUser')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Day15',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('receiver', models.OneToOneField(to='shipments.GenericUser')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Day28',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('receiver', models.OneToOneField(to='shipments.GenericUser')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Day31',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('receiver', models.OneToOneField(to='shipments.GenericUser')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Day38',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('receiver', models.OneToOneField(to='shipments.GenericUser')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Day7',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('receiver', models.OneToOneField(to='shipments.GenericUser')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='notification',
            name='email_content_html_file',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='email_mergevars',
            field=models.TextField(null=True, blank=True),
        ),
    ]
