# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('shipments', '0056_companyinvite_invite_accepted'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShipmentAssignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('parent_id', models.PositiveIntegerField()),
                ('assignee_id', models.PositiveIntegerField()),
                ('can_delegate', models.BooleanField(default=False)),
                ('notify', models.BooleanField(default=False)),
                ('r', models.BooleanField(default=False)),
                ('u', models.BooleanField(default=False)),
                ('d', models.BooleanField(default=False)),
                ('assignee_content_type', models.ForeignKey(related_name='shipment_assignment_assignee', to='contenttypes.ContentType')),
                ('assigner', models.ForeignKey(blank=True, to='shipments.GenericUser', null=True)),
                ('parent_content_type', models.ForeignKey(related_name='shipment_assignment_parent', to='contenttypes.ContentType')),
                ('shipment', models.ForeignKey(to='shipments.Shipment')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='shipmentassignment',
            unique_together=set([('shipment', 'assigner', 'assignee_id', 'assignee_content_type')]),
        ),
        migrations.AlterModelOptions(
            name='shipment',
            options={'permissions': (('view_shipment', 'View Shipment'),)},
        ),
        migrations.AddField(
            model_name='shipment',
            name='owner_user',
            field=models.ForeignKey(blank=True, to='shipments.GenericUser', null=True),
            preserve_default=True,
        ),
    ]
