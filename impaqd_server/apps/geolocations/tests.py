import unittest
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from django.core import exceptions

import random
from datetime import timedelta
from StringIO import StringIO
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from ..shipments.models.delivery_status import DeliveryStatus
from ..shipments.models.generic_user import GenericUser
from ..shipments.models.shipments import Shipment
from ..shipments.factories import (
    UserFactory, CarrierDriverFactory, ShipmentFactory, CarrierCompanyFactory)
from ..shipments.factories.generic_user_factory import (
    GenericUserFactory)

from .validators import RangeValidator, LatitudeValidator, LongitudeValidator
from .factories import GeolocationNoShipmentFactory
from .models import (
    Geolocation, pre_save_find_shipment, geolocation_trigger_arrivals)
from .serializers import GeolocationSerializer
from .views import GeolocationsCreateView

# Create your tests here.


class RangeValidatorTests(TestCase):
    @classmethod
    def setUpClass(cls):
        # call super, then add your code
        super(cls, RangeValidatorTests).setUpClass()

    @classmethod
    def tearDownClass(cls):
        # add your code first, then call super
        super(cls, RangeValidatorTests).tearDownClass()

    def setUp(self):
        self.lower = random.uniform(-1000, 0)
        self.upper = random.uniform(0, 1000)
        self.assertLess(self.lower, self.upper)
        self.target = RangeValidator(lower=self.lower, upper=self.upper)

    def tearDown(self):
        pass

    def test_range_validator_value_less_than_lower_bound(self):
        value = self.lower + random.uniform(-1000, 1)
        self.assertLess(value, self.lower)
        try:
            self.target(value)
            self.fail("Unexpected success")
        except exceptions.ValidationError:
            pass

    def test_range_validator_value_greater_than_upper_bound(self):
        value = self.upper + random.uniform(1, 1000)
        self.assertGreater(value, self.upper)
        try:
            self.target(value)
            self.fail("Unexpected success")
        except exceptions.ValidationError:
            pass

    def test_range_validator_value_within_bounds(self):
        value = random.uniform(self.lower, self.upper)
        self.assertGreater(value, self.lower)
        self.assertLess(value, self.upper)
        try:
            self.target(value)
        except serializers.ValidationError:
            self.fail("Unexpected failure")


class LatitudeValidatorTests(TestCase):
    @classmethod
    def setUpClass(cls):
        # call super, then add your code
        super(cls, LatitudeValidatorTests).setUpClass()

    @classmethod
    def tearDownClass(cls):
        # add your code first, then call super
        super(cls, LatitudeValidatorTests).tearDownClass()

    def setUp(self):
        self.target = LatitudeValidator()

    def tearDown(self):
        pass

    def test_latitiude_validator_is_range_validator(self):
        self.assertTrue(self.target, RangeValidator)

    def test_latitiude_validator_bounds(self):
        self.assertEqual(-90.0, self.target.lower)
        self.assertEqual(90.0, self.target.upper)


class LongitudeValidatorTests(TestCase):
    @classmethod
    def setUpClass(cls):
        # call super, then add your code
        super(cls, LongitudeValidatorTests).setUpClass()

    @classmethod
    def tearDownClass(cls):
        # add your code first, then call super
        super(cls, LongitudeValidatorTests).tearDownClass()

    def setUp(self):
        self.target = LongitudeValidator()

    def tearDown(self):
        pass

    def test_latitiude_validator_is_range_validator(self):
        self.assertTrue(self.target, RangeValidator)

    def test_latitiude_validator_bounds(self):
        self.assertEqual(-180.0, self.target.lower)
        self.assertEqual(180.0, self.target.upper)


class GeolocationTests(TestCase):
    @classmethod
    def setUpClass(cls):
        # call super, then add your code
        super(cls, GeolocationTests).setUpClass()

    @classmethod
    def tearDownClass(cls):
        # add your code first, then call super
        super(cls, GeolocationTests).tearDownClass()

    def setUp(self):
        self.target = GeolocationNoShipmentFactory.build()

    def tearDown(self):
        pass

    def test_geolocation(self):
        try:
            self.target.full_clean()
            self.assertTrue(True)
        except serializers.ValidationError as e:
            self.fail(e.messages)

    def test_geolocation_without_shipment_is_valid(self):
        try:
            self.target.full_clean()
            self.assertTrue(True)
        except serializers.ValidationError as e:
            self.fail(e.messages)

    def test_geolocation_pre_save_find_shipment_sets_shipment(self):
        self.assertIsNone(self.target.shipment)
        carrier = self.target.carrier
        status = random.choice(DeliveryStatus.ACTIVE_STATUSES)
        shipment = ShipmentFactory.create(carrier=carrier, delivery_status=status)
        self.target.timestamp = shipment.first_location.time_range.time_range_start
        pre_save_find_shipment(Geolocation, self.target, None)
        self.assertIsNotNone(self.target.shipment)
        self.assertEqual(shipment, self.target.shipment)

    def test_geolocation_pre_save_find_shipment_does_nothing_for_no_shipment(self):
        self.assertIsNone(self.target.shipment)
        self.assertFalse(Shipment.actives.all().exists())
        pre_save_find_shipment(Geolocation, self.target, None)
        self.assertIsNone(self.target.shipment)

    def test_geolocation_pre_save_find_shipment_for_multiple_results(self):
        self.assertIsNone(self.target.shipment)
        carrier = self.target.carrier
        status = random.choice(DeliveryStatus.ACTIVE_STATUSES)
        # Shipments must have same pickup and delivery dates.
        # Otherwise the ActiveShipmentManager will filter them out.
        shipmentA = ShipmentFactory.create(
            carrier=carrier, delivery_status=status, carrier_is_approved=True)

        # Clone TimeRange objects
        pick_up_time_info = shipmentA.first_location.time_range
        pick_up_time_info.pk = None
        pick_up_time_info.save()
        delivery_time_info = shipmentA.last_location.time_range
        delivery_time_info.pk = None
        delivery_time_info.save()
        shipmentB = ShipmentFactory.create(
            carrier=carrier, delivery_status=status, carrier_is_approved=True)
        shipmentB.first_location.time_range = pick_up_time_info
        shipmentB.first_location.save()
        shipmentB.last_location.time_range = delivery_time_info
        shipmentB.last_location.save()

        # Clone TimeRange objects
        pick_up_time_info = shipmentA.first_location.time_range
        pick_up_time_info.pk = None
        pick_up_time_info.save()
        delivery_time_info = shipmentA.last_location.time_range
        delivery_time_info.pk = None
        delivery_time_info.save()
        shipmentC = ShipmentFactory.create(
            carrier=carrier, delivery_status=status, carrier_is_approved=True)
        shipmentC.first_location.time_range = pick_up_time_info
        shipmentC.first_location.save()
        shipmentC.last_location.time_range = delivery_time_info
        shipmentC.last_location.save()

        self.assertGreater(shipmentC.updated_at, shipmentA.updated_at)
        self.assertGreater(shipmentC.updated_at, shipmentB.updated_at)
        self.target.timestamp = shipmentC.first_location.time_range.time_range_start
        pre_save_find_shipment(Geolocation, self.target, None)
        self.assertIsNotNone(self.target.shipment)
        self.assertEqual(shipmentC, self.target.shipment)

    def test_geolocation_pre_save_find_shipment_timestamp_in_range(self):
        self.assertIsNone(self.target.shipment)
        carrier = self.target.carrier
        status = DeliveryStatus.ENROUTE
        shipment = ShipmentFactory.create(carrier=carrier, delivery_status=status)
        self.target.timestamp = shipment.first_location.time_range.time_range_start
        pre_save_find_shipment(Geolocation, self.target, None)
        self.assertIsNotNone(self.target.shipment)
        self.assertEqual(shipment, self.target.shipment)

    def test_geolocation_pre_save_find_shipment_timestamp_too_early(self):
        self.assertIsNone(self.target.shipment)
        carrier = self.target.carrier
        status = DeliveryStatus.ENROUTE
        shipment = ShipmentFactory.create(carrier=carrier, delivery_status=status)
        self.target.timestamp = shipment.first_location.time_range.time_range_start - timedelta(hours=5)
        pre_save_find_shipment(Geolocation, self.target, None)
        self.assertIsNone(self.target.shipment)

    def test_geolocation_pre_save_find_shipment_timestamp_too_late(self):
        self.assertIsNone(self.target.shipment)
        carrier = self.target.carrier
        status = DeliveryStatus.ENROUTE
        shipment = ShipmentFactory.create(carrier=carrier, delivery_status=status)
        self.target.timestamp = shipment.first_location.time_range.time_range_end + timedelta(hours=5)
        pre_save_find_shipment(Geolocation, self.target, None)
        self.assertIsNone(self.target.shipment)

    def test_geolocation_trigger_arrivals_enroute(self):
        carrier = self.target.carrier
        status = DeliveryStatus.PENDING_PICKUP
        owner = GenericUserFactory()
        shipment = ShipmentFactory.create(
            carrier=carrier, carrier_is_approved=True, delivery_status=status,
            owner=owner.company)
        # Weird things happen when not loading first and last location from the
        # db first.
        first_location = Shipment.objects.get(pk=shipment.id).first_location
        self.target.timestamp = first_location.time_range.time_range_start + timedelta(minutes=5)
        self.target.shipment = shipment
        # ~10 miles
        self.target.latitude = first_location.latitude + 0.18
        self.target.longitude = first_location.longitude + 0.18
        geolocation_trigger_arrivals(
            Geolocation.__class__, self.target, True, False)
        self.assertEqual(
            self.target.shipment.delivery_status,
            DeliveryStatus.PENDING_PICKUP)
        self.assertIsNone(self.target.shipment.first_location.arrival_time)
        # ~2 miles
        self.target.latitude = first_location.latitude + 0.03
        self.target.longitude = first_location.longitude + 0.03
        geolocation_trigger_arrivals(
            Geolocation.__class__, self.target, True, False)
        self.assertEqual(
            self.target.shipment.delivery_status, DeliveryStatus.ENROUTE)
        self.target.shipment.first_location.refresh_from_db()
        self.assertEqual(
            self.target.shipment.first_location.arrival_time, self.target.timestamp)

    def test_geolocation_trigger_arrivals_delivered(self):
        # Only for two locations
        # TODO: similar test for more that two locations
        carrier = self.target.carrier
        status = DeliveryStatus.ENROUTE
        owner = GenericUserFactory()
        shipment = ShipmentFactory.create(
            carrier=carrier, carrier_is_approved=True, delivery_status=status,
            owner=owner.company)
        # Weird things happen when not loading first and last location from the
        # db first.
        first_location = Shipment.objects.get(pk=shipment.id).first_location
        last_location = Shipment.objects.get(pk=shipment.id).last_location
        first_location.arrival_time = first_location.time_range.time_range_start
        first_location.save()
        self.target.timestamp = last_location.time_range.time_range_start + timedelta(minutes=5)
        self.target.shipment = shipment
        # ~10 miles
        self.target.latitude = last_location.latitude + 0.18
        self.target.longitude = last_location.longitude + 0.18
        geolocation_trigger_arrivals(
            Geolocation.__class__, self.target, True, False)
        self.assertEqual(
            self.target.shipment.delivery_status,
            DeliveryStatus.ENROUTE)
        self.assertIsNone(self.target.shipment.last_location.arrival_time)
        # ~2 miles
        self.target.latitude = last_location.latitude + 0.03
        self.target.longitude = last_location.longitude + 0.03
        geolocation_trigger_arrivals(
            Geolocation.__class__, self.target, True, False)
        self.assertEqual(
            self.target.shipment.delivery_status, DeliveryStatus.DELIVERED)
        self.target.shipment.last_location.refresh_from_db()
        self.assertEqual(
            self.target.shipment.last_location.arrival_time, self.target.timestamp)

    @unittest.skip("Pending")
    def test_geolocation_post_save_dispatch_tasks(self):
        # sends update driver location task
        # sends shipment tracker task
        pass


class GeolocationSerializerTests(TestCase):
    @classmethod
    def setUpClass(cls):
        # call super, then add your code
        super(cls, GeolocationSerializerTests).setUpClass()

    @classmethod
    def tearDownClass(cls):
        # add your code first, then call super
        super(cls, GeolocationSerializerTests).tearDownClass()

    def setUp(self):
        self.geolocation = GeolocationNoShipmentFactory.build()
        serializer = GeolocationSerializer(self.geolocation)
        json_data = JSONRenderer().render(serializer.data)
        stream = StringIO(json_data)
        data = JSONParser().parse(stream)
        self.target = GeolocationSerializer(data=data)

    def tearDown(self):
        pass

    def test_geolocation_serializer_is_valid(self):
        self.assertTrue(self.target.is_valid())

    def test_geolocation_serializer_object(self):
        self.assertTrue(self.target.is_valid())
        new_geolocation = self.target.save()
        self.assertIsNotNone(new_geolocation)
        for f in self.geolocation._meta.fields:
            old_value = getattr(self.geolocation, f.attname)
            new_value = getattr(new_geolocation, f.attname)
            if f.attname == 'timestamp':
                self.assertTrue(timedelta(seconds=1) > old_value-new_value)
            elif f.attname != 'id':
                self.assertEqual(old_value, new_value)

    def test_geolocation_serializer_validate_latitude(self):
        latitude = 90.0 + random.random()
        try:
            self.target.validate_latitude(latitude)
            self.target.validate_latitude(-1 * latitude)
            self.fail("Unexpected success")
        except serializers.ValidationError:
            self.assertTrue(True)

        latitude = 90.0 - random.random()
        try:
            self.target.validate_latitude(latitude)
            self.target.validate_latitude(-1 * latitude)
            self.assertTrue(True)
        except serializers.ValidationError:
            self.fail("Unexpected ValidationError")

    def test_geolocation_serializer_validate_longitude(self):
        longitude = 180.0 + random.random()
        try:
            self.target.validate_longitude(longitude)
            self.target.validate_longitude(-1 * longitude)
            self.fail("Unexpected success")
        except serializers.ValidationError:
            self.assertTrue(True)

        longitude = 180.0 - random.random()
        try:
            self.target.validate_longitude(longitude)
            self.target.validate_longitude(-1 * longitude)
            self.assertTrue(True)
        except serializers.ValidationError:
            self.fail("Unexpected ValidationError")


class GeolocationsCreateViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        # call super, then add your code
        super(cls, GeolocationsCreateViewTests).setUpClass()

    @classmethod
    def tearDownClass(cls):
        # add your code first, then call super
        super(cls, GeolocationsCreateViewTests).tearDownClass()

    def setUp(self):
        self.driver = CarrierDriverFactory.create()
        self.user = self.driver.user
        self.carrier = CarrierCompanyFactory.create(owner=self.driver)
        self.geolocation = GeolocationNoShipmentFactory.build(driver=self.driver)

        serializer = GeolocationSerializer(self.geolocation)
        self.data = serializer.data
        self.data.pop('carrier')
        self.data.pop('driver')
        self.data.pop('shipment')
        self.data.pop('id')

        self.factory = APIRequestFactory()
        self.target = GeolocationsCreateView.as_view()

    def tearDown(self):
        pass
    
    def test_geolocations_create_view_post(self):
        request = APIRequestFactory().post('/api/geolocations/', self.data, format='json')
        force_authenticate(request, user=self.user)
        response = self.target(request)
        self.assertEqual(201, response.status_code)
        self.assertEqual(response.data['driver'], self.driver.pk)
        self.assertEqual(response.data['carrier'], self.driver.company.pk)

    def test_geolocations_create_view_post_no_data(self):
        request = APIRequestFactory().post('/api/geolocations/', None, format='json')
        force_authenticate(request, user=self.user)
        response = self.target(request)
        self.assertEqual(403, response.status_code)

    def test_geolocation_create_view_post_with_non_carrier_driver_user(self):
        user = UserFactory.create()
        self.assertFalse(GenericUser.objects.filter(user_id=user.pk).exists())
        request = APIRequestFactory().post('/api/geolocations/', self.data, format='json')
        force_authenticate(request, user=user)
        response = self.target(request)
        self.assertEqual(404, response.status_code)
