import unittest
from django.test.testcases import TestCase
from django.contrib.gis.geos import Point
from ...geolocations.factories import GeolocationNoShipmentFactory
from ..models.generic_user import GenericUser
from ..tasks import task_update_carrier_driver_geolocation


class TaskUpdateCarrierDriverGeolocationTests(TestCase):
    @classmethod
    def setUpClass(cls):
        # call super, then add your code
        super(cls, TaskUpdateCarrierDriverGeolocationTests).setUpClass()

    @classmethod
    def tearDownClass(cls):
        # add your code first, then call super
        super(cls, TaskUpdateCarrierDriverGeolocationTests).tearDownClass()

    def setUp(self):
        self.geolocation = GeolocationNoShipmentFactory.create()
        self.driver = self.geolocation.driver

    def tearDown(self):
        pass

    @unittest.skip("no longer relevant")
    def test_task_update_carrier_driver_geolocation_updates_last_location(self):
        previous = self.driver.last_location
        task_update_carrier_driver_geolocation(self.geolocation)
        expected = Point(self.geolocation.latitude, self.geolocation.longitude)
        driver = GenericUser.objects.get(pk=self.driver.pk)
        self.assertNotEqual(previous, driver.last_location)
        self.assertEqual(expected, driver.last_location)

    @unittest.skip("no longer relevant")
    def test_task_update_carrier_driver_geolocation_updates_last_location_timestamp(self):
        previous = self.driver.last_location_timestamp
        task_update_carrier_driver_geolocation(self.geolocation)
        expected = self.geolocation.timestamp
        driver = GenericUser.objects.get(pk=self.driver.pk)
        self.assertNotEqual(previous, driver.last_location_timestamp)
        self.assertEqual(expected, driver.last_location_timestamp)
