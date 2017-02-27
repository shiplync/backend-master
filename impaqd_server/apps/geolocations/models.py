from django.core.exceptions import MultipleObjectsReturned
from django.contrib.gis.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from ..shipments.models import (
    Shipment, GenericCompany, GenericUser, DeliveryStatus)
from ..shipments.models.common import build_unicode_string
from .validators import LatitudeValidator, LongitudeValidator
from ..shipments.tasks import task_update_geolocation_display_text
from ..shipments.models.locations import AbstractAddress
from math import sin, cos, acos, degrees, radians


# Create your models here.


class Geolocation(models.Model):
    latitude = models.FloatField(null=False, blank=False, validators=[LatitudeValidator()])
    longitude = models.FloatField(null=False, blank=False, validators=[LongitudeValidator()])
    altitude = models.FloatField(null=True, blank=True)
    accuracy = models.FloatField(null=True, blank=True)
    speed = models.FloatField(null=True, blank=True)
    course = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(null=True, blank=True)

    carrier = models.ForeignKey(GenericCompany, null=False, blank=True, db_index=True)
    driver = models.ForeignKey(GenericUser, null=False, blank=True, db_index=True)
    shipment = models.ForeignKey(Shipment, null=True, blank=True, db_index=True)
    display_text = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ("carrier", "driver", "timestamp")


@receiver(pre_save, sender=Geolocation)
def pre_save_find_shipment(sender, instance, raw, **kwargs):
    if not instance.shipment:
        try:
            instance.shipment = Shipment.actives.for_carrier_driver(
                instance.driver, instance.timestamp).get()
        except Shipment.DoesNotExist:
            pass
        except MultipleObjectsReturned:
            instance.shipment = Shipment.actives.for_carrier_driver(
                instance.driver, instance.timestamp).latest('updated_at')
        except Exception:
            import traceback
            print traceback.format_exc()


@receiver(post_save, sender=Geolocation)
def post_save_dispatch_tasks(sender, instance, created, raw, **kwargs):
    if not created:
        return


def get_distance_miles(l_lat, l_lon, g_lat, g_lon):
    distance_miles = (
        sin(radians(l_lat)) *
        sin(radians(g_lat)) +
        cos(radians(l_lat)) *
        cos(radians(g_lat)) *
        cos(radians(l_lon - g_lon)))
    distance_miles = (degrees(acos(distance_miles))) * 69.09
    return distance_miles


@receiver(post_save, sender=Geolocation)
def geolocation_trigger_arrivals(sender, instance, created, raw, **kwargs):
    if created:
        geo_threshold = 4.0  # miles
        if instance.shipment and instance.shipment.upcoming_location:
            l = instance.shipment.upcoming_location
            l_lat = l.latitude
            l_lon = l.longitude
            g_lat = instance.latitude
            g_lon = instance.longitude
            if get_distance_miles(l_lat, l_lon, g_lat, g_lon) < geo_threshold:
                l.arrival_time = instance.timestamp
                l.save()
                instance.shipment.save()  # Trigger shipment status change


@receiver(post_save, sender=Geolocation)
def post_save_update_display_text(sender, instance, raw, created, **kwargs):
    if created and not instance.display_text:
        task_update_geolocation_display_text(instance)


class CachedCoordinate(AbstractAddress):
    coordinate = models.PointField(geography=True)

    class Meta:
        ordering = ('-created_at',)

    @property
    def latitude(self):
        return round(self.coordinate.y, 10)

    @property
    def longitude(self):
        return round(self.coordinate.x, 10)


class CachedDistance(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_lat = models.DecimalField(max_digits=13, decimal_places=10)
    end_lat = models.DecimalField(max_digits=13, decimal_places=10)
    start_lon = models.DecimalField(max_digits=13, decimal_places=10)
    end_lon = models.DecimalField(max_digits=13, decimal_places=10)
    distance = models.DecimalField(
        max_digits=9, decimal_places=1)

    class Meta:
        ordering = ('-created_at',)

    def __unicode__(self):
        return build_unicode_string(self, ('distance',))
