import unittest
from mock import Mock, MagicMock, patch, sentinel
from django.test.testcases import TestCase

from faker import Faker
fake = Faker()

import pprint
pp = pprint.PrettyPrinter(indent=4)

from ..factories import CarrierDriverFactory, CarrierCompanyOwnerOperatorFactory, fake_base64, fake_image
from mixins import GenericUserTestMixin

class CarrierDriverTests(TestCase, GenericUserTestMixin):
    @classmethod
    def setUpClass(cls):
        # call super, then add your code
        super(cls, CarrierDriverTests).setUpClass()

    @classmethod
    def tearDownClass(cls):
        # add your code first, then call super
        super(cls, CarrierDriverTests).tearDownClass()

    def setUp(self):
        carrier_company = CarrierCompanyOwnerOperatorFactory.create()
        self.generic_user = CarrierDriverFactory.create(company=carrier_company) # extends generic user

    def tearDown(self):
        pass
