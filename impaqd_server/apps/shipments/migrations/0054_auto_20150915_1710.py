# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0053_auto_20150911_1333'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyInvite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('invitee_name', models.CharField(max_length=200, null=True, blank=True)),
                ('invitee_email', models.EmailField(max_length=75)),
                ('invitee_dot', models.IntegerField(max_length=10, null=True, blank=True)),
                ('invitee_company_type', models.IntegerField(default=0, choices=[(0, b'Unknown'), (1, b'Shipper'), (2, b'Carrier')])),
                ('inviter_company', models.ForeignKey(to='shipments.GenericCompany')),
                ('inviter_user', models.ForeignKey(blank=True, to='shipments.GenericUser', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompanyRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_inviter', models.BooleanField(default=True)),
                ('active', models.BooleanField(default=True)),
                ('hidden', models.BooleanField(default=False)),
                ('relation_from', models.ForeignKey(related_name='from_relations', to='shipments.GenericCompany')),
                ('relation_to', models.ForeignKey(related_name='to_relations', to='shipments.GenericCompany')),
                ('sibling', models.ForeignKey(blank=True, to='shipments.CompanyRelation', help_text=b'The corresponding CompanyRelation with relation_from and relation_to reversed', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='companyinvite',
            unique_together=set([('inviter_company', 'invitee_dot'), ('inviter_company', 'invitee_email')]),
        ),
        migrations.AddField(
            model_name='genericcompany',
            name='relations',
            field=models.ManyToManyField(to='shipments.GenericCompany', through='shipments.CompanyRelation'),
            preserve_default=True,
        ),
    ]
