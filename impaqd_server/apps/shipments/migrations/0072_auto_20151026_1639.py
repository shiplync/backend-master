# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def forward(apps, schema_editor):
    Person = apps.get_model('shipments', 'Person')
    GenericUser = apps.get_model('shipments', 'GenericUser')

    for p in Person.objects.all():
        p.phone_2 = '+1%s' % p.phone
        p.save()

    for u in GenericUser.objects.all():
        u.phone_2 = '+1%s' % u.phone
        u.save()


def backward(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0071_auto_20151026_1639'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
