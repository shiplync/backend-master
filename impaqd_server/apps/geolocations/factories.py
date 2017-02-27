from datetime import datetime
from pytz import timezone
import random
import factory
import factory.django

from faker import Faker

from django.db.models.signals import pre_save, post_save

from ..shipments.factories import CarrierDriverFactory
from .models import Geolocation

fake = Faker()


def now():
    tz = timezone(fake.timezone())
    return datetime.now(tz)


@factory.django.mute_signals(pre_save, post_save)
class GeolocationNoCarrierFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Geolocation

    latitude = factory.LazyAttribute(lambda g: float(fake.latitude()))
    longitude = factory.LazyAttribute(lambda g: float(fake.longitude()))
    altitude = factory.LazyAttribute(lambda g: random.uniform(0, 1000))
    accuracy = factory.LazyAttribute(lambda g: random.uniform(0, 10))
    speed = factory.LazyAttribute(lambda g: random.uniform(0, 20))
    course = factory.LazyAttribute(lambda g: random.uniform(0, 360))
    timestamp = factory.LazyAttribute(lambda g: now())


@factory.django.mute_signals(pre_save, post_save)
class GeolocationNoShipmentFactory(GeolocationNoCarrierFactory):
    class Meta:
        model = Geolocation

    driver = factory.SubFactory(CarrierDriverFactory)
    carrier = factory.LazyAttribute(lambda g: g.driver.company)

    @factory.post_generation
    def create_carrier_and_driver(self, create, extracted, **kwargs):
        '''
        Create Carrier and Driver (if they exist) as post_generation hook
        to insure they are created and inserted into database
        '''
        if self.driver:
            self.driver.save()
            self.driver_id = self.driver.pk
            self.carrier_id = self.driver.company.pk
