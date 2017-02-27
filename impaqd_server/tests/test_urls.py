from django.test import TestCase, RequestFactory

from django.core.urlresolvers import Resolver404, get_resolver


class URLTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        # call super, then add your code
        super(cls, URLTestCase).setUpClass()

    @classmethod
    def tearDownClass(cls):
        # call super, then add your code
        super(cls, URLTestCase).tearDownClass()

    def setUp(self):
        self.factory = RequestFactory()
        self.target = get_resolver(None)

    def tearDown(self):
        pass

    def test_api_users_url_resolves(self):
        try:
            match = self.target.resolve('/api/users/')
            self.assertEqual('users_list_view', match.url_name)
        except Resolver404:
            self.fail('Cannot resolve /api/users/')

    def test_api_geolocations_url_resolves(self):
        try:
            match = self.target.resolve('/api/geolocations/')
            self.assertEqual('geolocations_create_view', match.url_name)
        except Resolver404:
            self.fail('Cannot resolve /api/geolocations/')

    def test_api_shipments_id_geolocations_url_resolves(self):
        try:
            match = self.target.resolve('/api/shipments/1/geolocations/')
            self.assertEqual('shipment_geolocations_list_view', match.url_name)
        except Resolver404:
            self.fail('Cannot resolve /api/shipments/1/geolocations/')
