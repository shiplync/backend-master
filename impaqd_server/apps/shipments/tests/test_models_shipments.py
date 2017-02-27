import unittest
from django.test.testcases import TestCase
from guardian.core import ObjectPermissionChecker

from faker import Faker
fake = Faker()

import pprint
pp = pprint.PrettyPrinter(indent=4)

import random
from django.db.models.query import QuerySet, EmptyQuerySet
from django.contrib.gis.db import models
from ..models.delivery_status import DeliveryStatus
from ..models.shipments import (
    ActiveShipmentManager, shipment_post_save_set_groups,
    shipment_post_delete_remove_groups)
from ..models.generic_company import (
    CompanyGroupType, get_company_group)
from ..models import Shipment
from ..factories import ShipmentFactory, CarrierDriverFactory


class ShipmentTests(TestCase):
    @classmethod
    def setUpClass(cls):
        # call super, then add your code
        super(cls, ShipmentTests).setUpClass()

    @classmethod
    def tearDownClass(cls):
        # add your code first, then call super
        super(cls, ShipmentTests).tearDownClass()

    def setUp(self):
        self.target = ShipmentFactory()

    def tearDown(self):
        pass

    def test_shipment(self):
        self.assertIsNotNone(self.target)

    def test_add_remove_shipment_rud_to_poster(self):
        self.assertFalse(
            self.target.owner_user.user.has_perm(
                'view_shipment', self.target) or
            self.target.owner_user.user.has_perm(
                'change_shipment', self.target) or
            self.target.owner_user.user.has_perm(
                'delete_shipment', self.target))
        shipment_post_save_set_groups(
            Shipment.__class__, self.target, True, False)
        self.assertTrue(
            self.target.owner_user.user.has_perm(
                'view_shipment', self.target) or
            self.target.owner_user.user.has_perm(
                'change_shipment', self.target) or
            self.target.owner_user.user.has_perm(
                'delete_shipment', self.target))
        shipment_post_delete_remove_groups(
            Shipment.__class__, self.target)
        self.assertFalse(
            self.target.owner_user.user.has_perm(
                'view_shipment', self.target) or
            self.target.owner_user.user.has_perm(
                'change_shipment', self.target) or
            self.target.owner_user.user.has_perm(
                'delete_shipment', self.target))

    def test_add_remove_shipment_rud_to_group_company_id_managers(self):
        g = get_company_group(
            self.target.owner, CompanyGroupType.MANAGERS)
        checker = ObjectPermissionChecker(g)
        self.assertFalse(
            checker.has_perm(
                'view_shipment', self.target) or
            checker.has_perm(
                'change_shipment', self.target) or
            checker.has_perm(
                'delete_shipment', self.target))
        shipment_post_save_set_groups(
            Shipment.__class__, self.target, True, False)
        checker = ObjectPermissionChecker(g)
        self.assertTrue(
            checker.has_perm(
                'view_shipment', self.target) or
            checker.has_perm(
                'change_shipment', self.target) or
            checker.has_perm(
                'delete_shipment', self.target))
        shipment_post_delete_remove_groups(
            Shipment.__class__, self.target)
        checker = ObjectPermissionChecker(g)
        self.assertFalse(
            checker.has_perm(
                'view_shipment', self.target) or
            checker.has_perm(
                'change_shipment', self.target) or
            checker.has_perm(
                'delete_shipment', self.target))

    @unittest.expectedFailure
    def test_add_remove_shipment_r_to_group_company_id_all(self):
        """
        Expected failure: Currently we don't want all in company to have access
        to a shipment by default
        """
        g = get_company_group(
            self.target.owner, CompanyGroupType.ALL)
        checker = ObjectPermissionChecker(g)
        self.assertFalse(
            checker.has_perm('view_shipment', self.target))
        shipment_post_save_set_groups(
            Shipment.__class__, self.target, True, False)
        checker = ObjectPermissionChecker(g)
        self.assertTrue(
            checker.has_perm('view_shipment', self.target))
        shipment_post_delete_remove_groups(
            Shipment.__class__, self.target)
        checker = ObjectPermissionChecker(g)
        self.assertFalse(
            checker.has_perm('view_shipment', self.target))


class ActiveShipmentManagerTests(TestCase):
    @classmethod
    def setUpClass(cls):
        # call super, then add your code
        super(cls, ActiveShipmentManagerTests).setUpClass()
        for status in DeliveryStatus.ALL_STATUSES:
            for i in xrange(random.randrange(5, 15)):
                s = ShipmentFactory.create(delivery_status=status)
                s.save()

    @classmethod
    def tearDownClass(cls):
        # add your code first, then call super
        super(cls, ActiveShipmentManagerTests).tearDownClass()

    def setUp(self):
        self.target = Shipment.actives
        self.shipments = {}
        for status in DeliveryStatus.ALL_STATUSES:
            self.shipments[status] = Shipment.objects.filter(
                delivery_status=status)

    def tearDown(self):
        pass

    def test_active_shipment_manager_is_geomanager(self):
        self.assertTrue(issubclass(ActiveShipmentManager, models.GeoManager))

    def test_active_shipment_manager_returns_only_active_shipments(self):
        for s in self.target.all():
            self.assertIn(s.delivery_status, DeliveryStatus.ACTIVE_STATUSES)

    def test_active_shipment_manager_for_carrier_driver(self):
        driver = CarrierDriverFactory.create()
        queryset = self.target.for_carrier_driver(driver)
        self.assertTrue(isinstance(queryset, QuerySet))
        self.assertFalse(isinstance(queryset, EmptyQuerySet))
