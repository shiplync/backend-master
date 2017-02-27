# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0111_auto_20160502_1636'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShipmentCarrierAssignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('assignment', models.OneToOneField(null=True, blank=True, to='shipments.ShipmentAssignment')),
            ],
        ),
        migrations.CreateModel(
            name='ShipmentDriverAssignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('assignment', models.OneToOneField(null=True, blank=True, to='shipments.ShipmentAssignment')),
            ],
        ),
        migrations.AlterField(
            model_name='companyinvite',
            name='invitee_name',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
