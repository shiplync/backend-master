import random
from django.test.testcases import TestCase
from ..models.delivery_status import DeliveryStatus


class DeliveryStatusTests(TestCase):
    @classmethod
    def setUpClass(cls):
        # call super, then add your code
        super(cls, DeliveryStatusTests).setUpClass()

    @classmethod
    def tearDownClass(cls):
        # add your code first, then call super
        super(cls, DeliveryStatusTests).tearDownClass()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_delivery_status_constants(self):
        self.assertTrue(hasattr(DeliveryStatus, 'OPEN'))
        self.assertTrue(hasattr(DeliveryStatus, 'PENDING_PICKUP'))
        self.assertTrue(hasattr(DeliveryStatus, 'ENROUTE'))
        self.assertTrue(hasattr(DeliveryStatus, 'DELIVERED'))
        self.assertTrue(hasattr(DeliveryStatus, 'PENDING_APPROVAL'))

    def test_delivery_status_choices(self):
        self.assertTrue(hasattr(DeliveryStatus, 'CHOICES'))

    def test_delivery_status_valid(self):
        value = random.randint(DeliveryStatus.OPEN, DeliveryStatus.PENDING_APPROVAL)
        invalid_low = DeliveryStatus.OPEN - 1
        invalid_high = DeliveryStatus.PENDING_APPROVAL + 1
        self.assertTrue(DeliveryStatus.valid(value))
        self.assertFalse(DeliveryStatus.valid(invalid_low))
        self.assertFalse(DeliveryStatus.valid(invalid_high))

    def test_delivery_status_active_statuses(self):
        self.assertIn(DeliveryStatus.PENDING_PICKUP, DeliveryStatus.ACTIVE_STATUSES)
        self.assertIn(DeliveryStatus.ENROUTE, DeliveryStatus.ACTIVE_STATUSES)
        self.assertNotIn(DeliveryStatus.OPEN, DeliveryStatus.ACTIVE_STATUSES)
        self.assertNotIn(DeliveryStatus.DELIVERED, DeliveryStatus.ACTIVE_STATUSES)
        self.assertNotIn(DeliveryStatus.PENDING_APPROVAL, DeliveryStatus.ACTIVE_STATUSES)

