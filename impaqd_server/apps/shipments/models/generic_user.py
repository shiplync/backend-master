from django.db.models.signals import (
    post_save, pre_save, post_delete,
    pre_delete)
from django.db.models.query_utils import Q
from django.dispatch import receiver
from django.contrib.gis.db import models
from django.contrib.auth.models import User

from phonenumber_field.modelfields import PhoneNumberField

from .vehicle_type import VehicleType
from .tos_acceptance import TOSAcceptance
from .shipments import Platform, PlatformType
from .generic_company import CompanyGroupType, get_company_group
from .company_division import DivisionGroupType, get_division_group
from .common import full_user_name
from ..utils import update_user


class UserType(object):
    UNKNOWN = 'unknown'

    # BROKERS MANAGER LEVEL
    BROKER_MANAGER = 'brokermanager'
    # BROKERS SUPERVISOR LEVEL
    BROKER_SUPERVISOR = 'brokersupervisor'
    # BROKER REPRESENTATIVE LEVEL
    BROKER_REPRESENTATIVE = 'brokerrepresentative'

    # CARRIER MANAGER LEVEL
    CARRIER_MANAGER = 'carriermanager'
    # CARRIER SUPERVISOR LEVEL
    CARRIER_SUPERVISOR = 'carriersupervisor'
    # CARRIER REPRESENTATIVE LEVEL
    CARRIER_DRIVER = 'carrierdriver'

    CHOICES = (
        (UNKNOWN, 'Unknown'),

        (BROKER_MANAGER, 'Broker Manager'),
        (CARRIER_MANAGER, 'Admin'),

        (BROKER_SUPERVISOR, 'Broker Supervisor'),
        (CARRIER_SUPERVISOR, 'Dispatcher'),

        (BROKER_REPRESENTATIVE, 'Broker Representative'),
        (CARRIER_DRIVER, 'Driver'),
    )

    BROKER_CHOICES = (
        (BROKER_MANAGER, 'Manager'),
        (BROKER_SUPERVISOR, 'Team Supervisor'),
        (BROKER_REPRESENTATIVE, 'Sales Representative'),
    )

    CARRIER_CHOICES = (
        (CARRIER_MANAGER, 'Manager'),
        (CARRIER_SUPERVISOR, 'Dispatcher/Team Supervisor'),
        (CARRIER_DRIVER, 'Driver'),
    )

    MANAGERS = [
        BROKER_MANAGER, CARRIER_MANAGER]

    SUPERVISORS = [
        BROKER_SUPERVISOR, CARRIER_SUPERVISOR]

    REPRESENTATIVES = [
        BROKER_REPRESENTATIVE, CARRIER_DRIVER]

    VALID_TYPES = [
        BROKER_MANAGER, CARRIER_MANAGER, BROKER_SUPERVISOR, CARRIER_SUPERVISOR,
        BROKER_REPRESENTATIVE, CARRIER_DRIVER]

    @classmethod
    def valid(cls, type):
        return (type != cls.UNKNOWN)


class GenericUser(models.Model):
    company = models.ForeignKey('GenericCompany')
    user_type = models.CharField(
        max_length=200, choices=UserType.CHOICES, default=UserType.UNKNOWN)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email = models.EmailField(unique=True)
    user = models.OneToOneField(User, default=None, null=True, blank=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone = PhoneNumberField(null=True, blank=True)
    profile_photo = models.OneToOneField(
        'FileContext',
        on_delete=models.SET_NULL, null=True, blank=True)
    permissions = models.OneToOneField(
        'permissions.BasePermissionCollection',
        on_delete=models.SET_NULL, null=True, blank=True)
    last_location = models.PointField(geography=True, blank=True, null=True)
    last_location_timestamp = models.DateTimeField(blank=True, null=True)
    vehicle_type = models.IntegerField(
        choices=VehicleType.CHOICES,
        default=VehicleType.FLATBED, blank=True, null=True)
    tos_acceptance = models.OneToOneField(
        'TOSAcceptance', null=True, blank=True, on_delete=models.SET_NULL)
    inactive = models.BooleanField(default=False)

    def __unicode__(self):
        return self.email

    @property
    def name(self):
        return full_user_name(self)

    @property
    def division(self):
        if self.companydivision_set.count():
            return self.companydivision_set.all()[0]
        return None


@receiver(pre_save)
def genericuser_pre_save(sender, instance, raw, **kwargs):
    if sender == GenericUser:
        # Set permissions if user doesn't have a
        # BasePermissionCollection object
        if not instance.permissions:
            from impaqd_server.apps.permissions.models import (
                BasePermissionCollection)
            instance.permissions = BasePermissionCollection.objects.create(
                user_type=instance.user_type)
        # Convert email to all lower cases
        if isinstance(instance.email, basestring):
            instance.email = instance.email.lower()
            pass
        # Attach a TOSAcceptance object
        if not instance.tos_acceptance:
            instance.tos_acceptance = TOSAcceptance.objects.create()


@receiver(post_save)
def generic_user_post_save(sender, instance, created, raw, **kwargs):
    if sender == GenericUser:
        # Always save permissions on genericuser post_save
        if instance.permissions:
            instance.permissions.user_type = instance.user_type
            instance.permissions.save()
        # Update username and email on User object
        update_user(instance)
        # Attach/update a default email platform
        platform, created = Platform.objects.get_or_create(
            platform_type=PlatformType.EMAIL, user=instance,
            is_primary_email=True)
        platform.identifier = instance.email
        platform.save()
        if created:
            from ..tasks import (
                task_new_user_or_company_create_company_relations)
            task_new_user_or_company_create_company_relations.delay(instance)


def genericuser_set_company_groups(genericuser, groups_to_add):
    all_groups = CompanyGroupType.ALL_TYPES
    groups_to_remove = list(set(all_groups) - set(groups_to_add))
    for g in groups_to_add:
        group = get_company_group(genericuser.company, g)
        genericuser.user.groups.add(group)
    for g in groups_to_remove:
        group = get_company_group(genericuser.company, g)
        genericuser.user.groups.remove(group)
    # Remove all company groups that doesn't reflect the current company
    # (if user changed company)
    company_str = 'company_'
    company_pk_str = 'company_%i_' % genericuser.company.pk
    groups_to_remove = genericuser.user.groups.filter(
        name__startswith=company_str).filter(
            ~Q(name__startswith=company_pk_str))
    for g in groups_to_remove:
        genericuser.user.groups.remove(g)


def genericuser_set_division_groups(genericuser, group_types, divisions):
    division_str = 'division_'
    current_division_groups = genericuser.user.groups.filter(
        name__startswith=division_str)

    groups_to_add = []
    for d in divisions:
        for gt in group_types:
            group = get_division_group(d, gt)
            groups_to_add.append(group)

    groups_to_remove = list(set(current_division_groups) - set(groups_to_add))

    for g in groups_to_add:
        if g not in current_division_groups:
            genericuser.user.groups.add(g)

    for g in groups_to_remove:
        if g in current_division_groups:
            genericuser.user.groups.remove(g)


@receiver(post_save)
def genericuser_post_save_set_groups(sender, instance, created, raw, **kwargs):
    if sender == GenericUser:
        """
        Assign users to their respective groups
        """
        company_groups = []
        division_groups = []
        divisions = instance.companydivision_set.all()

        # Brokers
        if instance.user_type == UserType.BROKER_MANAGER:
            company_groups = [
                CompanyGroupType.ALL,
                CompanyGroupType.MANAGERS,
                CompanyGroupType.VIEW_INCOMING_SHIPMENTS]
            division_groups = [
                DivisionGroupType.ALL,
                DivisionGroupType.SUPERVISORS,
                DivisionGroupType.VIEW_INCOMING_SHIPMENTS]
        elif instance.user_type == UserType.BROKER_SUPERVISOR:
            company_groups = [
                CompanyGroupType.ALL]
            division_groups = [
                DivisionGroupType.ALL,
                DivisionGroupType.SUPERVISORS,
                DivisionGroupType.VIEW_INCOMING_SHIPMENTS]
        elif instance.user_type == UserType.BROKER_REPRESENTATIVE:
            company_groups = [
                CompanyGroupType.ALL]
            division_groups = [
                DivisionGroupType.ALL]

        # Carriers
        elif instance.user_type == UserType.CARRIER_MANAGER:
            company_groups = [
                CompanyGroupType.ALL,
                CompanyGroupType.MANAGERS,
                CompanyGroupType.VIEW_INCOMING_SHIPMENTS]
            division_groups = [
                DivisionGroupType.ALL,
                DivisionGroupType.SUPERVISORS,
                DivisionGroupType.VIEW_INCOMING_SHIPMENTS]
        elif instance.user_type == UserType.CARRIER_SUPERVISOR:
            company_groups = [
                CompanyGroupType.ALL]
            division_groups = [
                DivisionGroupType.ALL,
                DivisionGroupType.SUPERVISORS,
                DivisionGroupType.VIEW_INCOMING_SHIPMENTS]
        elif instance.user_type == UserType.CARRIER_DRIVER:
            company_groups = [
                CompanyGroupType.ALL]
            division_groups = [
                DivisionGroupType.ALL]

        # Unknown
        else:
            company_groups = [CompanyGroupType.ALL]
            division_groups = [DivisionGroupType.ALL]

        # Set groups
        genericuser_set_company_groups(instance, company_groups)
        genericuser_set_division_groups(instance, division_groups, divisions)


@receiver(pre_delete)
def generic_user_pre_delete(sender, instance, **kwargs):
    # Sender can be GenericUser or an inheriting model
    if sender == GenericUser:
        if (hasattr(instance, 'permissions') and
                instance.permissions is not None):
            instance.permissions.delete()
        if (hasattr(instance, 'profile_photo') and
                instance.profile_photo is not None):
            instance.profile_photo.delete()
        if (hasattr(instance, 'tos_acceptance') and
                instance.tos_acceptance is not None):
            instance.tos_acceptance.delete()
        if (hasattr(instance, 'userinvite') and
                instance.userinvite is not None):
            instance.userinvite.delete()


@receiver(post_delete)
def generic_user_post_delete(sender, instance, **kwargs):
    # Sender can be GenericUser or an inheriting model
    if sender == GenericUser:
        # Delete dangling user object
        if instance.user:
            instance.user.delete()
