import random
from datetime import datetime, timedelta
from django.test import TestCase

from ...geolocations.factories import GeolocationNoShipmentFactory
from ..serializers.shipment_geolocation import ShipmentGeolocationSerializer
from ..factories import (
    CarrierDriverFactory, ShipmentFactory,
    CarrierCompanyFactory)


class ShipmentGeolocationSerializerTests(TestCase):
    @classmethod
    def setUpClass(cls):
        # call super, then add your code
        super(cls, ShipmentGeolocationSerializerTests).setUpClass()

    @classmethod
    def tearDownClass(cls):
        # add your code first, then call super
        super(cls, ShipmentGeolocationSerializerTests).tearDownClass()

    def setUp(self):
        self.driver = CarrierDriverFactory.create()
        self.carrier = CarrierCompanyFactory.create(owner=self.driver)
        self.shipment = ShipmentFactory.create(carrier=self.carrier)
        timestamp = datetime.now() - timedelta(weeks=1)
        for x in xrange(random.randrange(10, 100)):
            GeolocationNoShipmentFactory.create(shipment=self.shipment, carrier=self.driver.company, driver=self.driver, timestamp=timestamp)
            timestamp += timedelta(hours=1)
        self.geolocation_qs = self.shipment.geolocation_set.get_queryset()
        self.target = ShipmentGeolocationSerializer(self.geolocation_qs, many=True)

    def tearDown(self):
        pass

    def test_shipment_geolocation_serializer_data_count(self):
        self.assertEqual(self.geolocation_qs.count(), len(self.target.data))

    def test_shipment_geolocation_serializer_limits_fields(self):
        for data in self.target.data:
            self.assertTrue(isinstance(data, dict))
            self.assertTrue('latitude' in data)
            self.assertTrue('longitude' in data)
            self.assertTrue('timestamp' in data)
            data.pop('latitude', None)
            data.pop('longitude', None)
            data.pop('timestamp', None)
            data.pop('display_text', None)
            self.assertFalse(data)
