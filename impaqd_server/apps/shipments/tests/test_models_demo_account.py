from django.test.testcases import TestCase

from ..models.demo_account import (
    demo_account_post_save, demo_account_pre_delete)
from ..factories.demo_account_factory import DemoAccountFactory


class DemoAccountTests(TestCase):
    @classmethod
    def setUpClass(cls):
        # call super, then add your code
        super(cls, DemoAccountTests).setUpClass()

    @classmethod
    def tearDownClass(cls):
        # add your code first, then call super
        super(cls, DemoAccountTests).tearDownClass()

    def setUp(self):
        self.demo_account = DemoAccountFactory.create()
        self.demo_account.no_of_shipments = 5

    def tearDown(self):
        pass

    def test_demo_account(self):
        self.assertIsNotNone(self.demo_account)

    def test_collections_empty_initially(self):
        self.assertIsNone(self.demo_account.company)

    def test_shipper_carrier_not_none_pre_save(self):
        demo_account_post_save(
            self.demo_account.__class__, self.demo_account, False, True)
        self.assertIsNotNone(self.demo_account.company)

    def test_shipper_carrier_none_pre_delete(self):
        pass
