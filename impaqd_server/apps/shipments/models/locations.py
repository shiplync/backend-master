from .common import (
    full_user_name, get_empty_required_fields, instance_has_changed,
    build_unicode_string)
from django.contrib.gis.db import models
from django.conf import settings
from django.db.models.signals import (
    post_save, pre_save, post_delete)
from django.dispatch import receiver
from impaqd_server.apps.shipments.validators import validate_zip_code, STATES
from timezone_field import TimeZoneField
from datetime import datetime, timedelta
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

import logging
LOG = logging.getLogger('impaqd')


class LocationType(object):
    UNKNOWN = 0
    PICKUP = 1
    PICKUP_DROPOFF = 2
    DROPOFF = 3

    CHOICES = (
        (UNKNOWN, 'Unknown'),
        (PICKUP, 'Pick up'),
        (PICKUP_DROPOFF, 'Pick up and drop off'),
        (DROPOFF, 'Drop off'),
    )

    VALID_TYPES = [PICKUP, PICKUP_DROPOFF, DROPOFF]


def update_shipment_locations_order(shipment):
    count = shipment.locations.count()
    locations = shipment.locations.all()
    shipment_dirty_flag = False
    for i, location in enumerate(locations):
        location_dirty_flag = False
        # Update first location
        if i == 0 and shipment.first_location != location:
            shipment.first_location = location
            shipment_dirty_flag = True
        # Update last location (if count > 1)
        elif i == count - 1:
            if shipment.last_location != location:
                shipment.last_location = location
                shipment_dirty_flag = True
            if location.next_location is not None:
                location.next_location = None
                location_dirty_flag = True
        # Update next location
        if i < count - 1 and location.next_location != locations[i+1]:
            location.next_location = locations[i+1]
            location_dirty_flag = True
        if location_dirty_flag:
            location.save()
    if shipment_dirty_flag:
        shipment.save()


class AbstractAddress(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    address = models.TextField(null=True, blank=True)
    address_2 = models.TextField(null=True, blank=True)
    zip_code = models.CharField(
        max_length=5, null=True,
        validators=[validate_zip_code], blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(
        max_length=2, null=True,
        choices=STATES, blank=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return build_unicode_string(self, ('city', 'state', 'zip_code',))


class AddressDetails(AbstractAddress):
    pass


class Location(models.Model):
    objects = models.GeoManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    location_type = models.IntegerField(
        choices=LocationType.CHOICES, default=LocationType.UNKNOWN)
    contact = models.OneToOneField('Person', null=True, blank=True)
    features = models.OneToOneField('ShipmentFeatures', null=True, blank=True)
    time_range = models.OneToOneField('TimeRange', null=True, blank=True)
    address_details = models.OneToOneField(
        'AddressDetails', null=True, blank=True)
    company_name = models.CharField(max_length=100, null=True, blank=True)
    dock = models.CharField(max_length=100, null=True, blank=True)
    appointment_id = models.CharField(
        max_length=100, null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    saved = models.BooleanField(
        help_text=u'Whether or not the user has saved the location',
        default=False)

    class Meta:
        abstract = True

    @property
    def empty_required_fields(self):
        required_fields = ['city', 'state', 'zip_code']
        return get_empty_required_fields(self, required_fields)

    def __unicode__(self):
        return build_unicode_string(self, ('address_details',))


@receiver(pre_save)
def location_init_fields(sender, instance, raw, **kwargs):
    if sender == ShipmentLocation or sender == SavedLocation:
        if not instance.address_details:
            instance.address_details = AddressDetails.objects.create()
        if not instance.contact:
            instance.contact = Person.objects.create()
        if not instance.features:
            instance.features = ShipmentFeatures.objects.create()
        if not instance.time_range:
            instance.time_range = TimeRange.objects.create()


class ShipmentLocation(Location):
    shipment = models.ForeignKey('Shipment', related_name='locations')
    arrival_time = models.DateTimeField(null=True, blank=True)
    next_location = models.ForeignKey(
        'ShipmentLocation', null=True, blank=True, on_delete=models.SET_NULL,
        related_name='prev_location')
    cached_distance = models.ForeignKey(
        'geolocations.CachedDistance',
        null=True, blank=True, on_delete=models.SET_NULL)
    cached_coordinate = models.ForeignKey(
        'geolocations.CachedCoordinate',
        null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ('location_type', 'time_range__time_range_end',)

    @property
    def distance_to_next_location(self):
        if self.cached_distance and self.cached_distance.distance:
            return self.cached_distance.distance
        else:
            return 0

    @property
    def latitude(self):
        if self.cached_coordinate:
            return self.cached_coordinate.latitude
        else:
            return 0

    @property
    def longitude(self):
        if self.cached_coordinate:
            return self.cached_coordinate.longitude
        else:
            return 0


@receiver(post_save, sender=ShipmentLocation)
def shipmentlocation_created_update_shipment(
        sender, instance, raw, created, **kwargs):
    if created:
        update_shipment_locations_order(instance.shipment)


@receiver(post_delete, sender=ShipmentLocation)
def shipmentlocation_deleted_update_shipment(sender, instance, **kwargs):
    update_shipment_locations_order(instance.shipment)


class SavedLocation(Location):
    owner = models.ForeignKey('GenericCompany', null=True, blank=True)
    # name of location for address management
    saved_location_name = models.CharField(
        max_length=100, null=True, blank=True)
    cached_coordinate = models.ForeignKey(
        'geolocations.CachedCoordinate',
        null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ('-updated_at',)


class Person(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    phone = PhoneNumberField(null=True, blank=True)

    @property
    def name(self):
        return full_user_name(self)

    @property
    def phone_country_code(self):
        return self.phone.country_code

    def __unicode__(self):
        return build_unicode_string(self, ('name',))


class TimeRange(models.Model):
    time_range_start = models.DateTimeField(blank=True, null=True)
    time_range_end = models.DateTimeField(blank=True, null=True)
    tz = TimeZoneField(default='US/Eastern')

    def __unicode__(self):
        if self.time_range_end:
            return str(self.time_range_end.date())
        else:
            return 'None'

    @property
    def empty_required_fields(self):
        required_fields = ['time_range_end']
        return get_empty_required_fields(self, required_fields)


@receiver(post_save, sender=TimeRange)
def timerange_update_shipment(sender, instance, raw, created, **kwargs):
    if not created and hasattr(instance, 'shipmentlocation'):
        update_shipment_locations_order(instance.shipmentlocation.shipment)


class ShipmentFeatures(models.Model):
    weight = models.FloatField(null=True, blank=True)
    extra_details = models.TextField(null=True, blank=True)

    palletized = models.BooleanField(default=False)
    pallet_number = models.IntegerField(null=True, blank=True)
    pallet_length = models.FloatField(null=True, blank=True)
    pallet_width = models.FloatField(null=True, blank=True)
    pallet_height = models.FloatField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
