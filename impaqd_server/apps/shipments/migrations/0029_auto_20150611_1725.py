# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.db.models.signals import post_save
from impaqd_server.apps.shipments.models.generic_user import generic_user_post_save


def forward_existing_tos(apps, schema_editor):
    post_save.disconnect(receiver=generic_user_post_save)
    TOSAcceptance = apps.get_model('shipments', 'TOSAcceptance')
    for t in TOSAcceptance.objects.all():
        if t.user and hasattr(t.user, 'tos_acceptance'):
            t.user.tos_acceptance = t
            t.user.save()
    post_save.connect(receiver=generic_user_post_save)


def backward_existing_tos(apps, schema_editor):
    pass


def forward_new_tos(apps, schema_editor):
    TOSAcceptance = apps.get_model('shipments', 'TOSAcceptance')
    GenericUser = apps.get_model('shipments', 'GenericUser')
    post_save.disconnect(receiver=generic_user_post_save)
    for u in GenericUser.objects.all():
        if not u.tos_acceptance:
            u.tos_acceptance = TOSAcceptance.objects.create()
            u.save()
    post_save.connect(receiver=generic_user_post_save)


def backward_new_tos(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0028_auto_20150609_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='genericuser',
            name='tos_acceptance',
            field=models.OneToOneField(blank=True, to='shipments.TOSAcceptance', null=True, on_delete=models.SET_NULL),
            preserve_default=True,
        ),
        migrations.RunPython(forward_existing_tos, backward_existing_tos),
        migrations.RunPython(forward_new_tos, backward_new_tos),
    ]
