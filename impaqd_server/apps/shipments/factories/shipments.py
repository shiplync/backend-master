import base64
import random
import uuid
from datetime import datetime, timedelta
from django.utils import timezone

from django.db.models.signals import (
    pre_save, post_save, pre_delete, post_delete)
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from django.db import transaction

import factory
import factory.django
from factory import post_generation

from faker import Faker

from ...geolocations.models import CachedCoordinate
from ..models import ShipmentLocation, Shipment
from ..models.shipments import ShipmentPayout, shipment_init_locations
from ..models.locations import (
    TimeRange, Person, ShipmentFeatures, AddressDetails, location_init_fields,
    LocationType, shipmentlocation_created_update_shipment)
from ..models.generic_company import GenericCompany, CompanyType
from ..models.generic_user import GenericUser, UserType
from ..models.vehicle_type import VehicleType
from ..validators import STATES

fake = Faker()

from .user_factory import UserFactory
from .generic_user_factory import GenericUserFactory


def fake_datetime(start_date='now', end_date='+1w'):
    return fake.date_time_between(start_date=start_date, end_date=end_date)


def fake_base64():
    return "/9j/4AAQSkZJRgABAQEASABIAAD/4QBARXhpZgAATU0AKgAAAAgAAYdpAAQAAAABAAAAGgAAAAAAAqACAAQAAAABAAAAAaADAAQAAAABAAAAAQAAAAD/2wBDAAEBAQEBAQEBAQEBAQEBAgMCAgICAgMCAwIDBAMEBAQDBAQEBQYFBAUGBQQEBQcGBgYHBwcHBAUICAgHCAYHBwf/2wBDAQEBAQIBAgMCAgMHBQQFBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwf/wAARCAABAAEDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD+/iiiigD/2Q=="


def fake_image():
    return base64.b64decode(fake_base64())


@factory.django.mute_signals(pre_save, post_save)
class ShipperCompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GenericCompany

    company_name = factory.LazyAttribute(lambda c: fake.company())
    insurance = None
    verified = True
    rejected = False
    owner = None  # set in test
    company_type = CompanyType.SHIPPER    


@factory.django.mute_signals(pre_save, post_save, pre_delete, post_delete)
class PersonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Person
    first_name = factory.LazyAttribute(lambda l: fake.first_name())
    last_name = factory.LazyAttribute(lambda l: fake.last_name())
    email = factory.LazyAttribute(lambda l: fake.email())
    # TODO: Add phone (PhoneNumberField)


@factory.django.mute_signals(pre_save, post_save)
class CarrierCompanyOwnerOperatorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GenericCompany

    company_name = factory.LazyAttribute(lambda c: fake.company())
    insurance = None
    verified = True
    rejected = False
    owner = None  # set in test
    dot = factory.LazyAttribute(lambda s: random.randint(1000000, 9999999))
    is_fleet = False
    max_requests = 1
    company_type = CompanyType.CARRIER


@factory.django.mute_signals(pre_save, post_save)
class CarrierCompanyFleetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GenericCompany

    company_name = factory.LazyAttribute(lambda c: fake.company())
    insurance = None
    verified = True
    rejected = False
    owner = None  # set in test
    dot = factory.LazyAttribute(lambda s: random.randint(1000000, 9999999))
    is_fleet = True
    max_requests = 100
    company_type = CompanyType.CARRIER


@factory.django.mute_signals(pre_save, post_save)
class CarrierCompanyFactory(factory.django.DjangoModelFactory):
    """
    Same as CarrierCompanyFleetFactory
    """
    class Meta:
        model = GenericCompany

    company_name = factory.LazyAttribute(lambda c: fake.company())
    insurance = None
    verified = True
    rejected = False
    owner = None  # set in test
    dot = factory.LazyAttribute(lambda s: random.randint(1000000, 9999999))
    is_fleet = True
    max_requests = 100
    company_type = CompanyType.CARRIER


@factory.django.mute_signals(pre_save, post_save)
class CarrierDriverFactory(GenericUserFactory):
    class Meta:
        model = GenericUser

    company = factory.SubFactory(CarrierCompanyOwnerOperatorFactory)
    created_at = factory.LazyAttribute(lambda s: s.user.date_joined)
    updated_at = factory.LazyAttribute(lambda s: s.created_at)
    vehicle_type = factory.LazyAttribute(lambda s: random.choice([v[0] for v in VehicleType.CHOICES]))
    user_type = UserType.CARRIER_DRIVER

    @factory.post_generation
    def create_company(self, created, extracted, **kwargs):
        '''
        Save the User and/or Company (if it exists) as a
        post_generation hook to insure it is created and inserted into
        the database
        '''
        if self.company:
            self.company.save()
            self.company_id = self.company.pk


@factory.django.mute_signals(pre_save, post_save)
class ShipperManagerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GenericUser

    company = factory.SubFactory(ShipperCompanyFactory)
    user = factory.SubFactory(UserFactory)
    created_at = factory.LazyAttribute(lambda s: s.user.date_joined)
    updated_at = factory.LazyAttribute(lambda s: s.created_at)
    first_name = factory.LazyAttribute(lambda s: s.user.first_name)
    last_name = factory.LazyAttribute(lambda s: s.user.last_name)
    phone = factory.LazyAttribute(lambda s: fake.phone_number())
    email = factory.LazyAttribute(lambda s: s.user.email)
    user_type = UserType.BROKER_MANAGER


class TimeRangeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TimeRange
    time_range_start = timezone.now()
    time_range_end = timezone.now()


@factory.django.mute_signals(pre_save, post_save, pre_delete, post_delete)
class ShipmentPayoutFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ShipmentPayout
    payout = factory.LazyAttribute(lambda l: random.randint(500, 3000))


@factory.django.mute_signals(pre_save, post_save, pre_delete, post_delete)
class ShipmentFeaturesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ShipmentFeatures


@factory.django.mute_signals(pre_save, post_save, pre_delete, post_delete)
class EmptyShipmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Shipment


@factory.django.mute_signals(pre_save, post_save, pre_delete, post_delete)
class AddressDetailsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AddressDetails

    address = factory.LazyAttribute(lambda l: fake.street_address())
    zip_code = factory.LazyAttribute(lambda l: fake.zipcode())
    city = factory.LazyAttribute(lambda l: fake.city())
    state = factory.LazyAttribute(lambda l: random.choice(STATES)[0])


@factory.django.mute_signals(pre_save, post_save, pre_delete, post_delete)
class CachedCoordinateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CachedCoordinate

    coordinate = factory.LazyAttribute(
        lambda l: Point(float(fake.latitude()), float(fake.longitude())))


@factory.django.mute_signals(pre_save, post_save)
class LocationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ShipmentLocation

    address_details = factory.SubFactory(AddressDetailsFactory)
    contact = factory.SubFactory(PersonFactory)
    cached_coordinate = factory.SubFactory(CachedCoordinateFactory)
    company_name = factory.LazyAttribute(lambda l: fake.name())
    features = factory.SubFactory(ShipmentFeaturesFactory)
    time_range = factory.SubFactory(TimeRangeFactory)

    @post_generation
    def post(obj, create, extracted, **kwargs):
        shipmentlocation_created_update_shipment(
            ShipmentLocation.__class__, obj, True, True)


@factory.django.mute_signals(pre_save, post_save, pre_delete, post_delete)
class ShipmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Shipment

    shipment_id = factory.LazyAttribute(lambda s: uuid.uuid4().hex)
    carrier = factory.SubFactory(CarrierCompanyOwnerOperatorFactory)
    owner = factory.SubFactory(ShipperCompanyFactory)
    owner_user = factory.SubFactory(GenericUserFactory)
    payout_info = factory.SubFactory(ShipmentPayoutFactory)

    @post_generation
    def post(obj, create, extracted, **kwargs):
        LocationFactory(shipment=obj, location_type=LocationType.PICKUP)
        LocationFactory(shipment=obj, location_type=LocationType.DROPOFF)
