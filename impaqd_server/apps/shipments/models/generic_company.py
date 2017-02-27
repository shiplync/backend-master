from django.db.models.signals import (
    pre_save, post_save, post_delete)
from django.dispatch import receiver
from django.contrib.gis.db import models
from django.contrib.auth.models import Group
from django.utils import timezone

from impaqd_server.apps.shipments.validators import STATES
from ...payments.models import Subscription


class CompanyType(object):
    UNKNOWN = 'unknown'
    SHIPPER = 'shipper'
    CARRIER = 'carrier'

    CHOICES = (
        (UNKNOWN, 'Unknown'),
        (SHIPPER, 'Shipper'),
        (CARRIER, 'Carrier')
    )

    @classmethod
    def valid(cls, type):
        return (type == cls.SHIPPER or type == cls.CARRIER)

    VALID_TYPES = [SHIPPER, CARRIER]


class CompanyGroupType(object):
    ALL = 'company_%i_all'
    MANAGERS = 'company_%i_managers'
    VIEW_INCOMING_SHIPMENTS = 'company_%i_view_incoming_shipments'

    CHOICES = (
        (ALL, 'All'),
        (MANAGERS, 'Managers'),
        (VIEW_INCOMING_SHIPMENTS, 'View incoming shipments')
    )

    @classmethod
    def valid(cls, type):
        return (
            type == cls.ALL or
            type == cls.MANAGERS or
            type == cls.VIEW_INCOMING_SHIPMENTS)

    ALL_TYPES = [ALL, MANAGERS, VIEW_INCOMING_SHIPMENTS]


def get_company_group(company, group_type):
    if not company or not company.id:
        return None
    g, created = Group.objects.get_or_create(
        name=(group_type % company.id))
    return g


class GenericCompany(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    company_name = models.CharField(max_length=200, null=True, blank=True)
    insurance = models.OneToOneField(
        'Insurance', related_name='company_insurance', null=True,
        blank=True)
    verified = models.BooleanField(default=True)
    rejected = models.BooleanField(default=False)
    registration_complete = models.BooleanField(default=False)
    owner = models.ForeignKey('GenericUser', null=True, blank=True)
    dot = models.IntegerField(
        unique=True, verbose_name="DOT", null=True, blank=True)
    is_fleet = models.BooleanField(default=False)
    max_requests = models.IntegerField(default=1)
    company_type = models.CharField(
        max_length=200, choices=CompanyType.CHOICES,
        default=CompanyType.UNKNOWN)
    relations = models.ManyToManyField(
        'self', through='CompanyRelation', symmetrical=False)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(
        max_length=2, null=True,
        choices=STATES, blank=True)
    logo = models.OneToOneField(
        'FileContext',
        on_delete=models.SET_NULL, null=True, blank=True)
    subscription = models.OneToOneField(
        'payments.Subscription', null=True, blank=True)

    @property
    def name(self):
        return (self.company_name if self.company_name else self.owner.name if
                self.owner else self.dot if self.dot else '')

    @property
    def remaining_user_invites(self):
        user_count = self.genericuser_set.filter(inactive=False).count()
        invite_count = self.userinvite_set.filter(user=None).count()
        allowance = self.subscription.no_users + self.subscription.no_trucks
        return allowance - user_count - invite_count

    def __unicode__(self):
        return (self.company_name if self.company_name else self.owner.name if
                self.owner else str(self.dot) if self.dot else '')


@receiver(pre_save, sender=GenericCompany)
def genericcompany_pre_save_create_subscription(
        sender, instance, raw, **kwargs):
    if not instance.subscription:
        instance.subscription = Subscription.objects.create()
        # Set trial
        instance.subscription.trial_start = timezone.now()
        instance.subscription.trial_length = 30
        instance.subscription.save()


@receiver(post_save, sender=GenericCompany)
def generic_company_post_save(sender, instance, created, raw, **kwargs):
    if created:
        from ..tasks import task_new_user_or_company_create_company_relations
        task_new_user_or_company_create_company_relations.delay(instance)


@receiver(post_save, sender=GenericCompany)
def genericcompany_post_save_create_groups(
        sender, instance, created, raw, **kwargs):
    Group.objects.get_or_create(
        name=CompanyGroupType.VIEW_INCOMING_SHIPMENTS % instance.id)
    Group.objects.get_or_create(name=CompanyGroupType.MANAGERS % instance.id)
    Group.objects.get_or_create(name=CompanyGroupType.ALL % instance.id)


@receiver(post_delete, sender=GenericCompany)
def genericcompany_post_delete_remove_groups(
        sender, instance, **kwargs):
    Group.objects.filter(
        name=CompanyGroupType.VIEW_INCOMING_SHIPMENTS % instance.id).delete()
    Group.objects.filter(name=CompanyGroupType.MANAGERS % instance.id).delete()
    Group.objects.filter(name=CompanyGroupType.ALL % instance.id).delete()
