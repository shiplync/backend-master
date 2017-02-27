# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0060_auto_20151008_0938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyinvite',
            name='invitee_dot',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='companyinvite',
            name='invitee_email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='demoaccount',
            name='connections',
            field=models.ManyToManyField(related_name='demo_account_companies', to='shipments.GenericCompany'),
        ),
        migrations.AlterField(
            model_name='demoaccount',
            name='dot',
            field=models.IntegerField(unique=True, null=True, verbose_name=b'DOT', blank=True),
        ),
        migrations.AlterField(
            model_name='demoaccount',
            name='email',
            field=models.EmailField(unique=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='genericcompany',
            name='dot',
            field=models.IntegerField(unique=True, null=True, verbose_name=b'DOT', blank=True),
        ),
        migrations.AlterField(
            model_name='genericuser',
            name='email',
            field=models.EmailField(unique=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='location',
            name='email',
            field=models.EmailField(max_length=254, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='savedlocation',
            name='email',
            field=models.EmailField(max_length=254, null=True, blank=True),
        ),
    ]
