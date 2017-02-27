from django.db.models.signals import (
    post_save, pre_save, post_delete)
from django.dispatch import receiver
from django.contrib.gis.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from guardian.shortcuts import assign_perm, remove_perm
from .generic_user import GenericUser
from .generic_company import (
    GenericCompany, CompanyGroupType, get_company_group)
from .company_division import (
    CompanyDivision, DivisionGroupType, get_division_group)
from ...notifications.models.shipment_assignment import ShipmentAssignmentNotif
from ..models.delivery_status import DeliveryStatus
from impaqd_server.apps.shipments import notifications


class ShipmentAssignment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    parent_limit = (
        models.Q(app_label='shipments', model='genericuser') |
        models.Q(app_label='shipments', model='companydivision') |
        models.Q(app_label='shipments', model='genericcompany') |
        models.Q(app_label='shipments', model='shipmentassignment'))
    parent_content_type = models.ForeignKey(
        ContentType, limit_choices_to=parent_limit,
        related_name='shipment_assignment_parent')
    parent_id = models.PositiveIntegerField()
    parent = GenericForeignKey('parent_content_type', 'parent_id')
    assignee_limit = models.Q(
        models.Q(app_label='shipments', model='genericuser') |
        models.Q(app_label='shipments', model='companydivision') |
        models.Q(app_label='shipments', model='genericcompany'))
    assignee_content_type = models.ForeignKey(
        ContentType, limit_choices_to=assignee_limit,
        related_name='shipment_assignment_assignee')
    assignee_id = models.PositiveIntegerField()
    assignee = GenericForeignKey('assignee_content_type', 'assignee_id')
    assigner = models.ForeignKey('GenericUser', null=True, blank=True)
    can_delegate = models.BooleanField(default=False)
    shipment = models.ForeignKey('shipment')
    notify = models.BooleanField(default=False)
    r = models.BooleanField(default=False)
    u = models.BooleanField(default=False)
    d = models.BooleanField(default=False)

    @property
    def carrier_assignment(self):
        if (hasattr(self, 'shipmentcarrierassignment') and
                self.shipmentcarrierassignment):
            return self.shipmentcarrierassignment.pk
        else:
            return None

    @property
    def driver_assignment(self):
        if (hasattr(self, 'shipmentdriverassignment') and
                self.shipmentdriverassignment):
            return self.shipmentdriverassignment.pk
        else:
            return None

    class Meta:
        pass

    def clean(self):
        if not (self.assignee_content_type.model == 'genericuser' or
                self.assignee_content_type.model == 'companydivision' or
                self.assignee_content_type.model == 'genericcompany'):
            raise ValidationError(_('Invalid assignee_content_type'))
        if (self.shipment and self.shipment.delivery_status in
                DeliveryStatus.CARRIER_APPROVED_STATUSES):
            raise ValidationError(
                _('This cannot be done when shipment '
                    'already has an approved carrier'))
        if not self.assigner and not self.id:
            raise ValidationError(
                _('ShipmentAssignments must be created with an assigner'))
        if (self.assigner and not
                self.assigner.user.has_perm('view_shipment', self.shipment)):
            raise ValidationError(
                _('Assigner must have permission to view the shipment'))
        if (ShipmentAssignment.objects.filter(
                shipment=self.shipment, assigner=self.assigner,
                assignee_content_type=self.assignee_content_type,
                assignee_id=self.assignee_id).count()):
            raise ValidationError(_('Assignment already exists'))


@receiver(pre_save, sender=ShipmentAssignment)
def shipmentassignment_pre_save_set_parrent(sender, instance, raw, **kwargs):
    # Set parent: Parent defines a dependency. Deleting the parent also
    # deletes the object.
    # First check that user has read permission to shipment
    if instance.assigner.user.has_perm('view_shipment', instance.shipment):
        # If shipment previously assigned to users company, set parent to
        # corresponding ShipmentAssignment
        ct = ContentType.objects.get_for_model(GenericCompany)
        qs = ShipmentAssignment.objects.filter(
            assignee_content_type=ct,
            assignee_id=instance.assigner.company.id,
            shipment=instance.shipment, can_delegate=True, r=True)
        if qs.count():
            instance.parent = qs[0]
            return
        # If shipment previously assigned to users division, set parent to
        # corresponding ShipmentAssignment
        divisions = instance.assigner.companydivision_set
        division_pks = [d.pk for d in divisions.all()]
        ct = ContentType.objects.get_for_model(CompanyDivision)
        qs = ShipmentAssignment.objects.filter(
            assignee_content_type=ct, assignee_id__in=division_pks,
            shipment=instance.shipment, can_delegate=True, r=True)
        if qs.count():
            instance.parent = qs[0]
            return
        # If shipment previously assigned to the user, set parent to
        # corresponding ShipmentAssignment
        ct = ContentType.objects.get_for_model(GenericUser)
        qs = ShipmentAssignment.objects.filter(
            assignee_content_type=ct,
            assignee_id=instance.assigner.id,
            shipment=instance.shipment, can_delegate=True, r=True)
        if qs.count():
            instance.parent = qs[0]
            return


@receiver(post_save, sender=ShipmentAssignment)
def shipmentassignment_post_save(sender, instance, created, raw, **kwargs):
    # Set object-level permission on assignee
    if instance.assignee.__class__ == GenericUser:
        u = instance.assignee.user
        if instance.r:
            assign_perm('view_shipment', u, instance.shipment)
        if instance.u:
            assign_perm('change_shipment', u, instance.shipment)
        if instance.d:
            assign_perm('delete_shipment', u, instance.shipment)
    elif instance.assignee.__class__ == CompanyDivision:
        g = get_division_group(
            instance.assignee, DivisionGroupType.VIEW_INCOMING_SHIPMENTS)
        if instance.r:
            assign_perm('view_shipment', g, instance.shipment)
        if instance.u:
            assign_perm('change_shipment', g, instance.shipment)
        if instance.d:
            assign_perm('delete_shipment', g, instance.shipment)
    elif instance.assignee.__class__ == GenericCompany:
        g = get_company_group(
            instance.assignee, CompanyGroupType.VIEW_INCOMING_SHIPMENTS)
        if instance.r:
            assign_perm('view_shipment', g, instance.shipment)
        if instance.u:
            assign_perm('change_shipment', g, instance.shipment)
        if instance.d:
            assign_perm('delete_shipment', g, instance.shipment)


@receiver(post_save, sender=ShipmentAssignment)
def shipmentassignment_post_save_notifications(
        sender, instance, created, raw, **kwargs):
    # Notify carrier
    if instance.assignee.__class__ == GenericUser:
        n = ShipmentAssignmentNotif.objects.create(
            shipment_assignment=instance, sender=instance.assigner)
        n.receivers = [instance.assignee]
        n.save()
        notifications.internal.shipment_assigned_carrier(
            instance.assigner.company, instance.assignee.company,
            instance.shipment, instance.assignee)
    elif instance.assignee.__class__ == CompanyDivision:
        n = ShipmentAssignmentNotif.objects.create(
            shipment_assignment=instance, sender=instance.assigner)
        group = get_division_group(
            instance.assignee, DivisionGroupType.VIEW_INCOMING_SHIPMENTS)
        n.receivers = [u.genericuser for u in group.user_set.all()]
        n.save()
        notifications.internal.shipment_assigned_carrier(
            instance.assigner.company, instance.assignee.company,
            instance.shipment)
    elif instance.assignee.__class__ == GenericCompany:
        n = ShipmentAssignmentNotif.objects.create(
            shipment_assignment=instance, sender=instance.assigner)
        group = get_company_group(
            instance.assignee, CompanyGroupType.VIEW_INCOMING_SHIPMENTS)
        n.receivers = [u.genericuser for u in group.user_set.all()]
        n.save()
        notifications.internal.shipment_assigned_carrier(
            instance.assigner.company, instance.assignee, instance.shipment)


@receiver(post_delete, sender=ShipmentAssignment)
def shipmentassignment_post_delete(sender, instance, **kwargs):
    # Remove object-level permission on assignee
    if instance.assignee:
        ct = ContentType.objects.get_for_model(instance.assignee.__class__)
        if instance.assignee.__class__ == GenericUser:
            existing_set = ShipmentAssignment.objects.filter(
                assignee_content_type=ct,
                assignee_id=instance.assignee.id,
                shipment=instance.shipment)
            u = instance.assignee.user
            if instance.r and existing_set.filter(r=True).count() == 0:
                remove_perm('view_shipment', u, instance.shipment)
            if instance.u and existing_set.filter(u=True).count() == 0:
                remove_perm('change_shipment', u, instance.shipment)
            if instance.d and existing_set.filter(d=True).count() == 0:
                remove_perm('delete_shipment', u, instance.shipment)
        elif instance.assignee.__class__ == CompanyDivision:
            existing_set = ShipmentAssignment.objects.filter(
                assignee_content_type=ct,
                assignee_id=instance.assignee.id,
                shipment=instance.shipment)
            g = get_division_group(
                instance.assignee, DivisionGroupType.VIEW_INCOMING_SHIPMENTS)
            if instance.r and existing_set.filter(r=True).count() == 0:
                remove_perm('view_shipment', g, instance.shipment)
            if instance.u and existing_set.filter(u=True).count() == 0:
                remove_perm('change_shipment', g, instance.shipment)
            if instance.d and existing_set.filter(d=True).count() == 0:
                remove_perm('delete_shipment', g, instance.shipment)
        elif instance.assignee.__class__ == GenericCompany:
            existing_set = ShipmentAssignment.objects.filter(
                assignee_content_type=ct,
                assignee_id=instance.assignee.id,
                shipment=instance.shipment)
            g = get_company_group(
                instance.assignee, CompanyGroupType.VIEW_INCOMING_SHIPMENTS)
            if instance.r and existing_set.filter(r=True).count() == 0:
                remove_perm('view_shipment', g, instance.shipment)
            if instance.u and existing_set.filter(u=True).count() == 0:
                remove_perm('change_shipment', g, instance.shipment)
            if instance.d and existing_set.filter(d=True).count() == 0:
                remove_perm('delete_shipment', g, instance.shipment)
            # Remove carrier from shipment when deleting the assignment
            # TODO: Remove this bit after implenenting ShipmentRequest
            if (instance.shipment.carrier and instance.shipment.carrier.id ==
                    instance.assignee.id):
                try:
                    instance.shipment.carrier = None
                    instance.shipment.save()
                except Exception:
                    pass


class ShipmentCarrierAssignment(models.Model):
    assignment = models.OneToOneField(
        'ShipmentAssignment', null=True, blank=True)


@receiver(post_save, sender=ShipmentCarrierAssignment)
def shipmentcarrierassignment_post_save(
        sender, instance, created, raw, **kwargs):
    if not created:
        return
    instance.assignment.shipment.carrier_assignment = instance
    instance.assignment.shipment.save()


@receiver(post_delete, sender=ShipmentCarrierAssignment)
def shipmentcarrierassignment_post_delete(sender, instance, **kwargs):
    if instance.assignment:
        instance.assignment.delete()


class ShipmentDriverAssignment(models.Model):
    assignment = models.OneToOneField(
        'ShipmentAssignment', null=True, blank=True)

    def clean(self):
        if self.assignment.id.get('shipment').driver_assignment:
            raise ValidationError(
                _('Shipment already has an assigned driver'))


@receiver(post_save, sender=ShipmentDriverAssignment)
def shipmentdriverassignment_post_save(
        sender, instance, created, raw, **kwargs):
    if not created:
        return
    instance.assignment.shipment.driver_assignment = instance
    instance.assignment.shipment.save()


@receiver(post_delete, sender=ShipmentDriverAssignment)
def shipmentdriverassignment_post_delete(sender, instance, **kwargs):
    if instance.assignment:
        instance.assignment.delete()
