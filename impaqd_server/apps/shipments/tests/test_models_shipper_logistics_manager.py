import unittest
from mock import Mock, MagicMock, patch, sentinel
from django.test.testcases import TestCase

from faker import Faker
fake = Faker()

import pprint
pp = pprint.PrettyPrinter(indent=4)

from ..factories import UserFactory, ShipperManagerFactory, ShipperCompanyFactory
from mixins import GenericUserTestMixin


class ShipperManagerTests(TestCase, GenericUserTestMixin):
    @classmethod
    def setUpClass(cls):
        # call super, then add your code
        super(cls, ShipperManagerTests).setUpClass()

    @classmethod
    def tearDownClass(cls):
        # add your code first, then call super
        super(cls, ShipperManagerTests).tearDownClass()

    def setUp(self):
        shipper_company = ShipperCompanyFactory.create()
        self.generic_user = ShipperManagerFactory.create(company=shipper_company) # extends generic user

    def tearDown(self):
        pass


