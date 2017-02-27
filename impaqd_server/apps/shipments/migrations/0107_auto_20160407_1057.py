# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0106_userinvite_assigner_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyDivision',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200, blank=True, null=True)),
                ('company', models.ForeignKey(to='shipments.GenericCompany')),
            ],
        ),
        migrations.CreateModel(
            name='CompanyDivisionMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('division', models.ForeignKey(to='shipments.CompanyDivision')),
                ('user', models.ForeignKey(to='shipments.GenericUser')),
            ],
        ),
        migrations.AddField(
            model_name='companydivision',
            name='members',
            field=models.ManyToManyField(to='shipments.GenericUser', through='shipments.CompanyDivisionMembership'),
        ),
    ]
