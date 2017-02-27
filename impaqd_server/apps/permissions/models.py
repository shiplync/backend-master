from django.contrib.gis.db import models
from django.contrib.auth.models import Permission
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from impaqd_server.apps.shipments.models.shipments import (
    Shipment)
from impaqd_server.apps.shipments.models.generic_user import UserType
from ..shipments.models.relations import CompanyInvite
from ..shipments.models.user_invite import UserInvite
from ..shipments.models.company_division import (
    CompanyDivision, CompanyDivisionMembership)
from ..shipments.models.generic_user import GenericUser
from ..shipments.models.generic_company import GenericCompany
from ..shipments.models.shipment_assignment import (
    ShipmentAssignment, ShipmentCarrierAssignment, ShipmentDriverAssignment)
from ..shipments.models.locations import SavedLocation

import logging
LOG = logging.getLogger('impaqd')


class BasePermissionCollection(models.Model):
    # Any instance of BasePermissionCollection must implement set_permissions()
    user_type = models.CharField(
        max_length=200, choices=UserType.CHOICES, default=UserType.UNKNOWN)

    def __unicode__(self):
        if hasattr(self, 'genericuser'):
            return self.genericuser.email
        else:
            return str(self.id)


def set_permission(
        permission_collection, model, rights, is_set=True, is_editable=False):
    rights_mapping = {'c': 'add', 'r': 'view', 'u': 'change', 'd': 'delete'}
    for r in rights:
        content_type = ContentType.objects.get_for_model(model)
        codename = '%s_%s' % (rights_mapping[r], content_type.model)
        p, created = Permission.objects.get_or_create(
            codename=codename, content_type=content_type)
        if created:
            p.name = 'Can %s %s' % (rights_mapping[r], content_type)
            p.save()
        b, created = BasePermission.objects.get_or_create(
            permission=p, permission_collection=permission_collection)
        if created:
            # If we just created the basepermission, set is_set and
            # is_editable according to the default values.
            b.is_set = is_set
            b.is_editable = is_editable
            b.save()


@receiver(post_save)
def base_permission_collection_post_save(
        sender, instance, raw, created, **kwargs):
    if sender == BasePermissionCollection:
        # Saving the BasePermissionCollection will add any new permissions to
        # that users permission collection.
        if not created:
            # Set permissions when saving collection. Not when creating it
            # (must be called by GenericUser object post_save signal).
            if instance.user_type == UserType.CARRIER_MANAGER:
                set_permission(instance, Shipment, 'crud')
                set_permission(instance, CompanyInvite, 'crud')
                set_permission(instance, UserInvite, 'crud')
                set_permission(instance, CompanyDivision, 'crud')
                set_permission(instance, CompanyDivisionMembership, 'crd')
                set_permission(instance, GenericUser, 'rud')
                set_permission(instance, GenericCompany, 'r')
                set_permission(instance, ShipmentAssignment, 'crud')
                set_permission(instance, SavedLocation, 'crud')
                set_permission(instance, ShipmentCarrierAssignment, 'crd')
                set_permission(instance, ShipmentDriverAssignment, 'crd')
            elif instance.user_type == UserType.CARRIER_SUPERVISOR:
                set_permission(instance, Shipment, 'crud')
                set_permission(instance, CompanyDivision, 'r')
                set_permission(instance, GenericUser, 'r')
                set_permission(instance, GenericCompany, 'r')
                set_permission(instance, ShipmentAssignment, 'crud')
                set_permission(instance, SavedLocation, 'crud')
                set_permission(instance, ShipmentCarrierAssignment, 'crd')
                set_permission(instance, ShipmentDriverAssignment, 'crd')
            elif instance.user_type == UserType.CARRIER_DRIVER:
                set_permission(instance, Shipment, 'r')
                set_permission(instance, CompanyDivision, 'r')
                set_permission(instance, GenericUser, 'r')
                set_permission(instance, GenericCompany, 'r')
                set_permission(instance, SavedLocation, 'r')

            if instance.user_type == UserType.BROKER_MANAGER:
                set_permission(instance, Shipment, 'crud')
                set_permission(instance, CompanyInvite, 'crud')
                set_permission(instance, UserInvite, 'crud')
                set_permission(instance, CompanyDivision, 'crud')
                set_permission(instance, CompanyDivisionMembership, 'crd')
                set_permission(instance, GenericUser, 'rud')
                set_permission(instance, GenericCompany, 'r')
                set_permission(instance, ShipmentAssignment, 'crud')
                set_permission(instance, SavedLocation, 'crud')
                set_permission(instance, ShipmentCarrierAssignment, 'crd')
            elif instance.user_type == UserType.BROKER_SUPERVISOR:
                set_permission(instance, Shipment, 'crud')
                set_permission(instance, CompanyDivision, 'r')
                set_permission(instance, GenericUser, 'r')
                set_permission(instance, GenericCompany, 'r')
                set_permission(instance, ShipmentAssignment, 'crud')
                set_permission(instance, SavedLocation, 'crud')
                set_permission(instance, ShipmentCarrierAssignment, 'crd')
            elif instance.user_type == UserType.BROKER_REPRESENTATIVE:
                set_permission(instance, Shipment, 'crud')
                set_permission(instance, CompanyDivision, 'r')
                set_permission(instance, GenericUser, 'r')
                set_permission(instance, GenericCompany, 'r')
                set_permission(instance, ShipmentAssignment, 'crud')
                set_permission(instance, SavedLocation, 'crud')
                set_permission(instance, ShipmentCarrierAssignment, 'crd')


class BasePermission(models.Model):
    name = models.CharField(max_length=100)
    permission = models.ForeignKey(Permission)
    is_set = models.BooleanField(default=False)
    is_editable = models.BooleanField(default=False)
    permission_collection = models.ForeignKey(
        'BasePermissionCollection', related_name='permissions')


@receiver(post_save, sender=BasePermission)
def base_permission_post_save(sender, instance, raw, created, **kwargs):
    instance.name = instance.permission.codename
    if instance.is_set:
        instance.permission_collection.genericuser.user.user_permissions.add(
            instance.permission)
    else:
        instance.permission_collection.genericuser.user.user_permissions.remove(
            instance.permission)


@receiver(pre_delete, sender=BasePermission)
def base_permission_pre_delete(sender, instance, **kwargs):
    if hasattr(instance.permission_collection, 'genericuser'):
        instance.permission_collection.genericuser.user.user_permissions.remove(
            instance.permission)
