from .common import get_empty_required_fields
from .locations import LocationType, ShipmentLocation
from .delivery_status import DeliveryStatus
from .equipment_tag import EquipmentTag
from django.contrib.gis.db import models
from django.db.models.signals import (
    pre_save, post_save, post_delete)
from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from guardian.shortcuts import assign_perm, remove_perm
import random

from rest_framework.authtoken.models import Token

from datetime import datetime, timedelta
from solo.models import SingletonModel

import logging
LOG = logging.getLogger('impaqd')


class ActiveShipmentManager(models.GeoManager):
    def get_queryset(self):
        return super(ActiveShipmentManager, self).get_queryset().filter(
            delivery_status__in=DeliveryStatus.ACTIVE_STATUSES)

    def for_carrier_driver(self, driver, timestamp=datetime.now()):
        # Active carrier shipments: Enroute or pending pickup and withing the
        # pickup-delivery time window (padded with 4 hours)
        try:
            carrier = driver.company
            time_window = timedelta(hours=4)
            return self.get_queryset().filter(
                carrier_id=carrier.pk,
                first_location__time_range__time_range_start__lte=timestamp+time_window,
                last_location__time_range__time_range_end__gte=timestamp-time_window)
        except ObjectDoesNotExist:
            import traceback
            print traceback.format_exc()
            return self.get_queryset().none()


class GlobalSettings(SingletonModel):
    shipment_id_counter = models.IntegerField(default=100)
    current_tos_version = models.IntegerField(default=0)


@receiver(pre_save, sender=GlobalSettings)
def global_settings_pre_save(sender, instance, raw, **kwargs):
    global_settings = None
    try:
        global_settings = GlobalSettings.objects.get()
    except ObjectDoesNotExist:
        return
    # When current_tos_version changes, update all tos objects
    # and reset tos_status if tos version has been changed
    if global_settings.current_tos_version != instance.current_tos_version:
        from .tos_acceptance import TOSAcceptance, TOSAcceptanceStatus
        for t in TOSAcceptance.objects.all():
            if t.tos_version < global_settings.current_tos_version:
                t.tos_status = TOSAcceptanceStatus.UNSET
                t.tos_version = global_settings.current_tos_version
                t.save()


class Shipment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    shipment_id = models.CharField(
        max_length=32, null=True, blank=True,
        help_text="Identifier for shipment. Not same as database primary key.")
    carrier = models.ForeignKey(
        'GenericCompany', null=True, blank=True,
        related_name='active_shipments')
    carrier_is_approved = models.BooleanField(default=False)
    owner = models.ForeignKey('GenericCompany', blank=True, null=True)
    owner_user = models.ForeignKey('GenericUser', blank=True, null=True)
    comments = models.TextField(null=True, blank=True)
    next_trip_dist_update = models.DateTimeField(auto_now_add=True)
    delivery_status = models.IntegerField(
        choices=DeliveryStatus.CHOICES, default=DeliveryStatus.OPEN)
    payout_info = models.OneToOneField('ShipmentPayout', null=True)
    bol_number = models.CharField(max_length=100, null=True, blank=True)

    first_location = models.OneToOneField(
        'ShipmentLocation', null=True, blank=True, on_delete=models.SET_NULL,
        related_name='shipment_first_location', help_text='Read only')
    last_location = models.OneToOneField(
        'ShipmentLocation', null=True, blank=True, on_delete=models.SET_NULL,
        related_name='shipment_last_location', help_text='Read only')

    carrier_assignment = models.OneToOneField(
        'ShipmentCarrierAssignment', null=True, blank=True,
        on_delete=models.SET_NULL)
    driver_assignment = models.OneToOneField(
        'ShipmentDriverAssignment', null=True, blank=True,
        on_delete=models.SET_NULL)
    objects = models.GeoManager()
    actives = ActiveShipmentManager()

    @property
    def location_count(self):
        return self.locations.count()

    @property
    def locations_completed(self):
        return self.locations.exclude(arrival_time__isnull=True).count()

    @property
    def upcoming_location(self):
        # First location that doesnt have an arrival_time
        for l in self.locations.all():
            if l.arrival_time is None:
                return l
        return None

    @property
    def first_pickup_occured(self):
        # Dont use self.first_location to avoid invalid cached instances
        count = self.locations.count()
        if count and self.locations.all()[0].arrival_time:
            return True
        else:
            return False

    @property
    def last_delivery_occured(self):
        # Dont use self.last_location to avoid invalid cached instances
        count = self.locations.count()
        if count and self.locations.all()[count-1].arrival_time:
            return True
        else:
            return False

    @property
    def trip_distance(self):
        distance = 0
        locations = self.locations.all()
        for index, location in enumerate(locations):
            if (len(locations) > 0 and index < len(locations)-1 and
                    location.distance_to_next_location is None):
                return 0
            else:
                distance = distance + location.distance_to_next_location
        return distance

    @property
    def carrier_driver(self):
        from .generic_user import UserType
        if self.carrier and (
                self.carrier.owner.user_type == UserType.CARRIER_DRIVER or
                self.carrier.owner.user_type == UserType.CARRIER_MANAGER):
            return self.carrier.owner
        else:
            return None

    @property
    def equipmenttags(self):
        return EquipmentTag.objects.filter(
            assignee_content_type=ContentType.objects.get(model='shipment'),
            assignee_id=self.id)

    @property
    def empty_required_fields(self):
        required_fields = ['payout_info']
        return get_empty_required_fields(self, required_fields)

    @property
    def assigned_companies_count(self):
        return self.shipmentassignment_set.filter(
            assignee_content_type=ContentType.objects.get(
                model='genericcompany')).count()

    @property
    def pending_requests_count(self):
        # TODO: Use ShipmentRequests model
        return 1 if self.carrier and not self.carrier_is_approved else 0

    @property
    def assigned_carrier(self):
        if self.carrier_assignment and self.carrier_assignment.assignment:
            return self.carrier_assignment.assignment.assignee
        else:
            return None

    @property
    def assigned_driver(self):
        if (self.driver_assignment and
                self.driver_assignment.assignment):
            return self.driver_assignment.assignment.assignee
        else:
            return None

    def __unicode__(self):
        return self.shipment_id

    class Meta:
        ordering = ('-pk',)
        # For ShipmentAssignment (view shipment is not a default permission)
        permissions = (
            ('view_shipment', 'View Shipment'),
        )


@receiver(pre_save, sender=Shipment)
def shipment_init_fields(sender, instance, raw, **kwargs):
    # Init payout_info
    if instance.payout_info is None:
        instance.payout_info = ShipmentPayout.objects.create()


@receiver(pre_save, sender=Shipment)
def shipment_set_status(sender, instance, raw, **kwargs):
    instance._delivery_status_changed = False
    if instance.last_delivery_occured and instance.carrier \
            and instance.carrier_is_approved:
        if instance.delivery_status == DeliveryStatus.ENROUTE:
            instance._delivery_status_changed = True
        # Shipment is delivered
        instance.delivery_status = DeliveryStatus.DELIVERED
    elif instance.first_pickup_occured and instance.carrier \
            and instance.carrier_is_approved:
        if instance.delivery_status == DeliveryStatus.PENDING_PICKUP:
            instance._delivery_status_changed = True
        # Shipment is picked up
        instance.delivery_status = DeliveryStatus.ENROUTE
    elif instance.carrier and instance.carrier_is_approved:
        if instance.delivery_status == DeliveryStatus.PENDING_APPROVAL:
            instance._delivery_status_changed = True
        # Shipment is claimed and shipper has approved carrier
        instance.delivery_status = DeliveryStatus.PENDING_PICKUP
    elif instance.carrier and not instance.carrier_is_approved:
        # Shipment is claimed and shipper has not approved carrier yet
        if instance.delivery_status == DeliveryStatus.OPEN:
            instance._delivery_status_changed = True
        instance.delivery_status = DeliveryStatus.PENDING_APPROVAL
    else:
        # Shipment was just created or carrier released shipment.
        # Reset all shipment
        instance.delivery_status = DeliveryStatus.OPEN
        instance.carrier_is_approved = False


@receiver(post_save, sender=Shipment)
def shipment_init_locations(sender, instance, created, raw, **kwargs):
    if created and instance.locations.count() == 0:
        ShipmentLocation.objects.create(
            shipment=instance, location_type=LocationType.PICKUP)
        ShipmentLocation.objects.create(
            shipment=instance, location_type=LocationType.DROPOFF)


@receiver(pre_save, sender=Shipment)
def shipment_init_shipment_id(sender, instance, raw, **kwargs):
    if not instance.shipment_id:
        # Currently shipment id generation doesn't work during testing when
        # using django solo).
        from django.conf import settings
        if settings.TESTING:
            instance.shipment_id = random.randint(1000000000000, 9999999999999)
        else:
            # Increment counter
            global_settings = GlobalSettings.objects.get()
            global_settings.shipment_id_counter += 1
            global_settings.save()
            # Assign id to shipment
            instance.shipment_id = global_settings.shipment_id_counter


@receiver(post_save, sender=Shipment)
def shipment_notifications(sender, instance, raw, created, **kwargs):
    pass
#     if instance.delivery_status == 1 and created:
#         # Shipment was just created
#         from impaqd_server.apps.shipments import notifications
#         notifications.internal.shipment_posted(instance, instance.owner)
#     if instance.delivery_status == 4 and instance._delivery_status_changed:
#         from impaqd_server.apps.shipments import notifications
#         notifications.shippers.shipment_delivered(
#             instance, instance.owner, instance.carrier)
#         notifications.internal.shipment_delivered(
#             instance, instance.owner, instance.carrier)
#     if instance.delivery_status == 3 and instance._delivery_status_changed:
#         from impaqd_server.apps.shipments import notifications
#         notifications.shippers.shipment_enroute(
#             instance, instance.owner, instance.carrier)
#         notifications.internal.shipment_enroute(
#             instance, instance.owner, instance.carrier)
#     if instance.delivery_status == 2 and instance._delivery_status_changed:
#         pass
#     if instance.delivery_status == 5 and instance._delivery_status_changed:
#         from impaqd_server.apps.shipments import notifications
#         notifications.shippers.shipment_requested(
#             instance, instance.owner, instance.carrier)
#         notifications.internal.shipment_requested(
#             instance, instance.owner, instance.carrier)


@receiver(post_save, sender=Shipment)
def shipment_post_save_set_groups(sender, instance, raw, created, **kwargs):
    from .generic_company import CompanyGroupType, get_company_group
    """
    assign shipment to owner, managers and company
    """
    # Assign to owner_user
    assign_perm('view_shipment', instance.owner_user.user, instance)
    assign_perm('change_shipment', instance.owner_user.user, instance)
    assign_perm('delete_shipment', instance.owner_user.user, instance)
    # Assign to managers
    g = get_company_group(instance.owner, CompanyGroupType.MANAGERS)
    assign_perm('view_shipment', g, instance)
    assign_perm('change_shipment', g, instance)
    assign_perm('delete_shipment', g, instance)
    # Assign to rest of company
    # g = get_company_group(instance.owner, CompanyGroupType.ALL)
    # assign_perm('view_shipment', g, instance)


@receiver(post_delete, sender=Shipment)
def shipment_post_delete_remove_groups(sender, instance, **kwargs):
    from .generic_company import CompanyGroupType, get_company_group
    """
    assign shipment to owner, managers and company
    """
    if hasattr(instance, 'owner_user') and instance.owner_user:
        # Remove from owner_user
        remove_perm('view_shipment', instance.owner_user.user, instance)
        remove_perm('change_shipment', instance.owner_user.user, instance)
        remove_perm('delete_shipment', instance.owner_user.user, instance)
    if hasattr(instance, 'owner') and instance.owner:
        # Remove from managers
        g = get_company_group(instance.owner, CompanyGroupType.MANAGERS)
        remove_perm('view_shipment', g, instance)
        remove_perm('change_shipment', g, instance)
        remove_perm('delete_shipment', g, instance)
        # Remove from rest of company
        g = get_company_group(instance.owner, CompanyGroupType.ALL)
        remove_perm('view_shipment', g, instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class PlatformType(object):
    EMAIL = 1
    IOS = 2
    ANDROID = 3

    CHOICES = (
        (EMAIL, 'Email'),
        (IOS, 'iOS'),
        (ANDROID, 'Android'),
    )


class Platform(models.Model):
    user = models.ForeignKey('GenericUser')
    platform_type = models.IntegerField(choices=PlatformType.CHOICES)
    identifier = models.CharField(
        max_length=512, help_text="UDID, email etc.", default="")
    allow_notifications = models.BooleanField(default=True)
    is_primary_email = models.BooleanField(
        default=False,
        help_text="In sync with the users email. Only one platform needs to have this field set to True")

    def __unicode__(self):
        return self.user.email


@receiver(pre_save, sender=Platform)
def platform_pre_save(sender, instance, raw, **kwargs):
    if instance.platform_type != PlatformType.EMAIL:
        instance.is_primary_email = False


class ShipmentPayout(models.Model):
    payout = models.DecimalField(
        max_digits=9, decimal_places=2, null=True, blank=True, default=0)
    comments = models.TextField(null=True, blank=True)

    @property
    def payout_distance(self):
        if self.payout and self.shipment.trip_distance:
            return self.payout / self.shipment.trip_distance
        else:
            return 0

    @property
    def empty_required_fields(self):
        required_fields = ['payout']
        return get_empty_required_fields(self, required_fields)


class ShipmentRequest(models.Model):
    shipment = models.ForeignKey('Shipment')
    carrier = models.ForeignKey('GenericCompany')
    driver = models.ForeignKey('GenericUser', null=True, blank=True)
    rejected = models.BooleanField(default=False)

    def __unicode__(self):
        return "{shipment: %s}" % self.shipment


@receiver(pre_save, sender=ShipmentRequest)
def update_shipment_request_fields(sender, instance, raw, **kwargs):
    # Don't save driver if it doesn't belong to the company
    if instance.driver and instance.carrier.pk != instance.driver.company.pk:
        instance.driver = None
