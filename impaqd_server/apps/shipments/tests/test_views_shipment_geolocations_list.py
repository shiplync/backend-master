import unittest
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

import pytz
import random
from datetime import datetime, timedelta

from ...geolocations.factories import GeolocationNoShipmentFactory
from ..views.shipments import shipment_geolocations_list_view
from ..factories import (
    CarrierDriverFactory, ShipmentFactory, ShipperCompanyFactory,
    ShipperManagerFactory, CarrierCompanyFactory)

import pprint
pp = pprint.PrettyPrinter(indent=4)

# Create your tests here.


class ShipmentGeolocationsListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        # call super, then add your code
        super(cls, ShipmentGeolocationsListViewTestCase).setUpClass()

    @classmethod
    def tearDownClass(cls):
        # call super, then add your code
        super(cls, ShipmentGeolocationsListViewTestCase).tearDownClass()

    def setUp(self):
        self.driver = CarrierDriverFactory.create()
        self.carrier = CarrierCompanyFactory.create(owner=self.driver)
        shippermanager = ShipperManagerFactory.create()
        shippercompany = ShipperCompanyFactory.create(owner=shippermanager)
        self.shipment = ShipmentFactory.create(carrier=self.carrier, owner=shippercompany)
        timestamp = datetime.now() - timedelta(weeks=1)
        for x in xrange(random.randrange(10, 100)):
            GeolocationNoShipmentFactory.create(shipment=self.shipment, carrier=self.driver.company, driver=self.driver, timestamp=timestamp)
            timestamp += timedelta(hours=1)

        self.factory = APIRequestFactory()
        self.path = '/api/shipments/%d/geolocations/' % (self.shipment.pk)

    def tearDown(self):
        pass

    @unittest.expectedFailure
    def test_shipment_geolocations_list_view_get_returns_401_for_non_shipment_shipper(self):
        self.assertNotEqual(self.driver.user, self.shipment.shipper_owner.user)
        request = self.factory.get(self.path, format='json')
        force_authenticate(request, user=self.driver.user)
        response = shipment_geolocations_list_view(request, pk=self.shipment.pk)
        self.assertEqual(401, response.status_code)

    def test_shipment_geolocations_list_view_get_returns_200_for_shipment_shipper(self):
        request = self.factory.get(self.path, format='json')
        force_authenticate(request, user=self.shipment.owner.owner.user)
        response = shipment_geolocations_list_view(request, self.shipment.pk)
        self.assertEqual(200, response.status_code)

    def test_shipment_geolocations_list_view_get_returns_shipment_geolocation_serializer_list_ordered_by_timestamp(self):
        request = self.factory.get(self.path, format='json')
        force_authenticate(request, user=self.shipment.owner.owner.user)
        response = shipment_geolocations_list_view(request, self.shipment.pk)
        parsed_data = response.data
        self.assertTrue(isinstance(parsed_data, list))
        timestamp = datetime.min.replace(tzinfo=pytz.utc)
        for data in parsed_data:
            data_ts = data['timestamp']
            self.assertLess(timestamp, data_ts)
            timestamp = data_ts
