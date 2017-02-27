import unittest
import random
from django.test.testcases import TestCase
from ..models.vehicle_type import VehicleType


class VehicleTypeTests(TestCase):
    @classmethod
    def setUpClass(cls):
        # call super, then add your code
        super(cls, VehicleTypeTests).setUpClass()

    @classmethod
    def tearDownClass(cls):
        # add your code first, then call super
        super(cls, VehicleTypeTests).tearDownClass()

    def setUp(self):
        pass

    def tearDown(self):
        pass
    @unittest.skip("no longer relevant")
    def test_vehicle_type_constants(self):
        self.assertTrue(hasattr(VehicleType, 'FLATBED'))
        self.assertTrue(hasattr(VehicleType, 'REEFER'))
        self.assertTrue(hasattr(VehicleType, 'VAN'))
        self.assertTrue(hasattr(VehicleType, 'POWER_ONLY'))

    @unittest.skip("no longer relevant")
    def test_vehicle_type_choices(self):
        self.assertTrue(hasattr(VehicleType, 'CHOICES'))
    
    @unittest.skip("no longer relevant")
    def test_vehicle_type_valid(self):
        value = random.randint(VehicleType.FLATBED, VehicleType.POWER_ONLY)
        invalid_low = VehicleType.FLATBED - 1
        invalid_high = VehicleType.POWER_ONLY + 1
        self.assertTrue(VehicleType.valid(value))
        self.assertFalse(VehicleType.valid(invalid_low))
        self.assertFalse(VehicleType.valid(invalid_high))
