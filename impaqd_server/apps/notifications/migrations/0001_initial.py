# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('shipments', '0107_auto_20160407_1057'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('parent_object_id', models.PositiveIntegerField()),
                ('sender_email', models.EmailField(max_length=254, null=True, blank=True)),
                ('sender_name', models.CharField(max_length=200, null=True, blank=True)),
                ('receiver_name', models.CharField(max_length=200, null=True, blank=True)),
                ('receiver_email', models.EmailField(max_length=254, null=True, blank=True)),
                ('email_subject', models.CharField(max_length=256, null=True, blank=True)),
                ('email_content_html', models.TextField(null=True, blank=True)),
                ('email_content_raw', models.TextField(null=True, blank=True)),
                ('parent_content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('receiver', models.ForeignKey(related_name='notifications_received', blank=True, to='shipments.GenericUser', null=True)),
                ('sender', models.ForeignKey(related_name='notifications_sent', blank=True, to='shipments.GenericUser', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ShipmentAssignmentNotif',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('receivers', models.ManyToManyField(related_name='shipmentassignmentnotif_inbox', to='shipments.GenericUser')),
                ('sender', models.ForeignKey(to='shipments.GenericUser')),
                ('shipment_assignment', models.ForeignKey(to='shipments.ShipmentAssignment')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserInviteNotif',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('receiver_email', models.EmailField(max_length=254)),
                ('receiver_name', models.CharField(max_length=200)),
                ('invite', models.ForeignKey(to='shipments.UserInvite')),
                ('sender', models.ForeignKey(to='shipments.GenericUser')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
