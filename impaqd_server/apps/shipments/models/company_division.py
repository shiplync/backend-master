from django.db import models
from django.db.models.signals import (
    post_save, pre_save, post_delete)
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class DivisionGroupType(object):
    ALL = 'division_%i_all'
    SUPERVISORS = 'division_%i_supervisors'
    VIEW_INCOMING_SHIPMENTS = 'division_%i_view_incoming_shipments'

    CHOICES = (
        (ALL, 'All'),
        (SUPERVISORS, 'Supervisors'),
        (VIEW_INCOMING_SHIPMENTS, 'View incoming shipments')
    )

    @classmethod
    def valid(cls, type):
        return (
            type == cls.ALL or
            type == cls.SUPERVISORS or
            type == cls.VIEW_INCOMING_SHIPMENTS)

    ALL_TYPES = [ALL, SUPERVISORS, VIEW_INCOMING_SHIPMENTS]


def get_division_group(division, group_type):
    if not division or not division.id:
        return None
    g, created = Group.objects.get_or_create(
        name=(group_type % division.id))
    return g


class CompanyDivision(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=30)
    company = models.ForeignKey('GenericCompany')
    members = models.ManyToManyField(
        'GenericUser', through='CompanyDivisionMembership')

    class Meta:
        ordering = ('name',)

    @property
    def members_count(self):
        return self.members.count()


@receiver(post_save, sender=CompanyDivision)
def companydivision_post_save_create_groups(
        sender, instance, created, raw, **kwargs):
    Group.objects.get_or_create(
        name=DivisionGroupType.VIEW_INCOMING_SHIPMENTS % instance.id)
    Group.objects.get_or_create(
        name=DivisionGroupType.SUPERVISORS % instance.id)
    Group.objects.get_or_create(name=DivisionGroupType.ALL % instance.id)


@receiver(post_delete, sender=CompanyDivision)
def companydivision_post_delete_remove_groups(
        sender, instance, **kwargs):
    Group.objects.filter(
        name=DivisionGroupType.VIEW_INCOMING_SHIPMENTS % instance.id).delete()
    Group.objects.filter(
        name=DivisionGroupType.SUPERVISORS % instance.id).delete()
    Group.objects.filter(name=DivisionGroupType.ALL % instance.id).delete()


class CompanyDivisionMembership(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    division = models.ForeignKey('CompanyDivision', on_delete=models.CASCADE)
    user = models.ForeignKey('GenericUser', on_delete=models.CASCADE)

    def clean(self):
        if self.division.company.pk != self.user.company.pk:
            raise ValidationError(_(
                'Users can only be assigned to divisions in their own '
                'company'))


@receiver(post_save, sender=CompanyDivisionMembership)
def companydivisionmembership_post_save_set_groups(
        sender, instance, created, raw, **kwargs):
    from impaqd_server.apps.shipments.models.generic_user import (
        GenericUser, genericuser_post_save_set_groups)
    genericuser_post_save_set_groups(
        GenericUser, instance.user, False, False)


@receiver(post_save, sender=CompanyDivisionMembership)
def companydivisionmembership_post_save_delete_existing(
        sender, instance, created, raw, **kwargs):
    """Currently users can only belong to one division. That cat easily be changed
    by removing this signal.
    """
    if created:
        CompanyDivisionMembership.objects.filter(
            user=instance.user).exclude(pk=instance.pk).delete()


@receiver(post_delete, sender=CompanyDivisionMembership)
def companydivisionmembership_post_delete_set_groups(
        sender, instance, **kwargs):
    from impaqd_server.apps.shipments.models.generic_user import (
        GenericUser, genericuser_post_save_set_groups)
    genericuser_post_save_set_groups(
        GenericUser, instance.user, False, False)
