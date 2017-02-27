import unittest
from mock import Mock, MagicMock, patch
from django.test.testcases import TestCase
from datetime import timedelta
from django.utils import timezone

from faker import Faker
fake = Faker()

import pprint
pp = pprint.PrettyPrinter(indent=4)

from ..factories import LocationFactory, ShipmentFactory
from ..models.locations import LocationType
from ..models.shipments import Shipment, shipment_init_locations


class LocationTests(TestCase):
    @classmethod
    def setUpClass(cls):
        # call super, then add your code
        super(cls, LocationTests).setUpClass()

    @classmethod
    def tearDownClass(cls):
        # add your code first, then call super
        super(cls, LocationTests).tearDownClass()

    def setUp(self):
        t = timezone.now()
        self.shipment = ShipmentFactory()
        self.shipment.first_location.time_range.time_range_start = t
        self.shipment.first_location.time_range.time_range_end = t
        self.shipment.last_location.time_range.time_range_start = (
            t + timedelta(days=3))
        self.shipment.last_location.time_range.time_range_end = (
            t + timedelta(days=3))
        pass

    def tearDown(self):
        pass

    def test_location_fields(self):
        self.location = LocationFactory.create(shipment=self.shipment)
        self.assertIsNotNone(self.location)
        self.assertIsNotNone(self.location.time_range)
        self.assertIsNotNone(self.location.contact)
        self.assertIsNotNone(self.location.features)
        self.assertIsNotNone(self.location.address_details)
        self.assertIsNotNone(self.location.shipment)

    def test_signal_creates_locations(self):
        self.shipment.locations.all().delete()
        self.shipment.refresh_from_db()
        self.assertIsNone(self.shipment.first_location)
        self.assertIsNone(self.shipment.last_location)
        self.assertEqual(self.shipment.locations.count(), 0)

        shipment_init_locations(
            Shipment.__class__, self.shipment, True, False)
        self.shipment.refresh_from_db()
        self.assertIsNotNone(self.shipment.first_location)
        self.assertIsNotNone(self.shipment.last_location)
        self.assertEqual(self.shipment.locations.count(), 2)

    def test_shipment_first_and_last_location(self):
        self.assertIsNotNone(self.shipment.first_location)
        self.assertIsNotNone(self.shipment.last_location)

        self.assertEqual(
            self.shipment.locations.all()[0],
            self.shipment.first_location)
        self.assertEqual(
            self.shipment.locations.all()[1],
            self.shipment.last_location)

        self.assertEqual(
            self.shipment.first_location.location_type,
            LocationType.PICKUP)
        self.assertEqual(
            self.shipment.last_location.location_type,
            LocationType.DROPOFF)

        self.shipment.first_location.refresh_from_db()
        self.assertEqual(
            self.shipment.first_location.next_location,
            self.shipment.last_location)
        self.assertEqual(self.shipment.last_location.next_location, None)

    def test_shipment_location_properties(self):
        self.assertEqual(self.shipment.location_count, 2)
        self.assertEqual(self.shipment.locations_completed, 0)
        self.assertEqual(
            self.shipment.upcoming_location, self.shipment.first_location)

    def test_add_remove_first_location(self):
        # Create location
        l1 = self.shipment.first_location
        # l2 = self.shipment.last_location
        l_new = LocationFactory.create(
            shipment=self.shipment, location_type=LocationType.PICKUP)
        l_new.time_range.time_range_end = (
            self.shipment.first_location.time_range.time_range_end +
            timedelta(days=-1))
        l_new.time_range.save()
        l_new.refresh_from_db()
        l_new.save()

        # Test
        self.assertEqual(self.shipment.location_count, 3)
        self.assertEqual(l_new.next_location, l1)
        self.assertEqual(self.shipment.first_location, l_new)
        self.assertEqual(self.shipment.upcoming_location, l_new)

        # Delete location
        l_new.delete()

        # Test
        self.assertEqual(self.shipment.location_count, 2)
        self.assertEqual(self.shipment.first_location, l1)
        self.assertEqual(self.shipment.upcoming_location, l1)

    def test_add_remove_mid_location(self):
        # Create location
        l1 = self.shipment.first_location
        l2 = self.shipment.last_location
        l_new = LocationFactory.create(
            shipment=self.shipment, location_type=LocationType.PICKUP_DROPOFF)
        l_new.time_range.time_range_end = (
            self.shipment.first_location.time_range.time_range_end +
            timedelta(days=+1))
        l_new.time_range.save()
        l_new.refresh_from_db()
        l_new.save()

        # Test
        l1.refresh_from_db()
        self.assertEqual(self.shipment.location_count, 3)
        self.assertEqual(l1.next_location, l_new)
        self.assertEqual(l_new.next_location, l2)
        self.assertEqual(self.shipment.first_location, l1)
        self.assertEqual(self.shipment.last_location, l2)
        self.assertEqual(self.shipment.upcoming_location, l1)

        # Delete location
        l_new.delete()

        # Test
        l1.refresh_from_db()
        self.assertEqual(self.shipment.location_count, 2)
        self.assertEqual(l1.next_location, l2)

    def test_add_remove_last_location(self):
        # Create location
        # l1 = self.shipment.first_location
        l2 = self.shipment.last_location
        l_new = LocationFactory.create(
            shipment=self.shipment, location_type=LocationType.DROPOFF)
        l_new.time_range.time_range_end = (
            self.shipment.first_location.time_range.time_range_end +
            timedelta(days=+4))
        l_new.time_range.save()
        l_new.refresh_from_db()
        l_new.save()

        # Test
        l2.refresh_from_db()
        self.assertEqual(self.shipment.location_count, 3)
        self.assertEqual(l2.next_location, l_new)
        self.assertEqual(l_new.next_location, None)
        self.assertEqual(self.shipment.last_location, l_new)

        # Delete location
        l_new.delete()

        # Test
        l2.refresh_from_db()
        self.assertEqual(self.shipment.location_count, 2)
        self.assertEqual(l2.next_location, None)
        self.assertEqual(self.shipment.last_location, l2)
