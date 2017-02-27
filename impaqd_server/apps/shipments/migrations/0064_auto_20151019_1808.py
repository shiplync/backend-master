# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('shipments', '0063_auto_20151019_1205'),
    ]

    operations = [
        migrations.CreateModel(
            name='EquipmentTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('tag_category', models.IntegerField(default=1, choices=[(1, b'Trailer type'), (2, b'Extra trailer equipment')])),
                ('tag_type', models.IntegerField(default=1, choices=[(1, b'Flatbed'), (2, b'Van'), (3, b'Reefer'), (1000, b'Tarps'), (1002, b'Vented')])),
                ('assignee_id', models.PositiveIntegerField()),
                ('assignee_content_type', models.ForeignKey(related_name='equipment_tag_assignee', to='contenttypes.ContentType')),
                ('assigner', models.ForeignKey(blank=True, to='shipments.GenericUser', null=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='equipmenttag',
            unique_together=set([('assignee_id', 'assignee_content_type', 'tag_type', 'tag_category')]),
        ),
    ]
