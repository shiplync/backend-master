import random
from django.test.testcases import TestCase
from impaqd_server.apps.shipments.factories.company_invite_factory import (
    CompanyInviteFactory)
from impaqd_server.apps.shipments.factories.generic_user_factory import (
    GenericUserFactory)
from impaqd_server.apps.shipments.factories.generic_company_factory import (
    UnknownCompanyFactory)
from impaqd_server.apps.shipments.factories.shipment_assignment_factory import (
    ShipmentAssignmentFactory)
from ...factories.company_division_factory import (
    CompanyDivisionFactory, CompanyDivisionMembershipFactory)
from impaqd_server.apps.shipments.factories.shipments import (
    ShipperCompanyFactory)
from impaqd_server.apps.shipments.models.relations import (
    CompanyInvite, company_invite_post_save, CompanyRelation)
from impaqd_server.apps.shipments.models.generic_user import (
    GenericUser, generic_user_post_save)
from impaqd_server.apps.shipments.models.generic_company import (
    GenericCompany, generic_company_post_save, CompanyGroupType, get_company_group)
from impaqd_server.apps.shipments.models.company_division import (
    CompanyDivision, DivisionGroupType, get_division_group)
from impaqd_server.apps.shipments.models.shipment_assignment import (
    ShipmentAssignment, shipmentassignment_post_save,
    shipmentassignment_post_delete)


class ShipmentAssignmentTest(TestCase):
    @classmethod
    def setUpClass(cls):
        # call super, then add your code
        super(cls, ShipmentAssignmentTest).setUpClass()

    @classmethod
    def tearDownClass(cls):
        # add your code first, then call super
        super(cls, ShipmentAssignmentTest).tearDownClass()

    def setUp(self):
        self.parent = ShipperCompanyFactory()

        self.assignee_u = GenericUserFactory()
        self.target_u = ShipmentAssignmentFactory(
            parent=self.parent, assignee=self.assignee_u, r=True)

        self.assignee_c = UnknownCompanyFactory(
            owner=GenericUserFactory())
        self.target_c = ShipmentAssignmentFactory(
            parent=self.parent, assignee=self.assignee_c, r=True)

        self.assignee_d = CompanyDivisionFactory()
        CompanyDivisionMembershipFactory(
            division=self.assignee_d, user=self.assignee_u)
        self.target_d = ShipmentAssignmentFactory(
            parent=self.parent, assignee=self.assignee_d, r=True)

    def tearDown(self):
        pass

    def test_shipment_assignment_sets_permission_user(self):
        self.assertFalse(
            self.assignee_u.user.has_perm('view_shipment', self.target_u.shipment))
        shipmentassignment_post_save(
            ShipmentAssignment.__class__, self.target_u, True, False)
        self.assertTrue(
            self.assignee_u.user.has_perm('view_shipment', self.target_u.shipment))

    def test_shipment_assignment_removes_permission_user(self):
        shipmentassignment_post_save(
            ShipmentAssignment.__class__, self.target_u, True, False)
        self.assertTrue(
            self.assignee_u.user.has_perm('view_shipment', self.target_u.shipment))
        shipmentassignment_post_delete(
            ShipmentAssignment.__class__, self.target_u)
        # Test that user still has permission, if an existing
        # shipmentassignment exists
        self.assertTrue(
            self.assignee_u.user.has_perm('view_shipment', self.target_u.shipment))
        self.target_u.delete()
        self.assertFalse(
            self.assignee_u.user.has_perm('view_shipment', self.target_u.shipment))

    def test_shipment_assignment_sets_and_removes_permission_company(self):
        g = get_company_group(
            self.assignee_c, CompanyGroupType.VIEW_INCOMING_SHIPMENTS)
        u = self.assignee_c.owner
        u.user.groups.add(g)
        shipmentassignment_post_save(
            ShipmentAssignment.__class__, self.target_c, True, False)
        self.assertTrue(
            u.user.has_perm('view_shipment', self.target_c.shipment))
        shipmentassignment_post_delete(
            ShipmentAssignment.__class__, self.target_c)
        # Test that user still has permission, if an existing
        # shipmentassignment exists
        self.assertTrue(
            u.user.has_perm('view_shipment', self.target_c.shipment))
        self.target_c.delete()
        self.assertFalse(
            u.user.has_perm('view_shipment', self.target_c.shipment))

    def test_shipment_assignment_sets_and_removes_permission_division(self):
        g = get_division_group(
            self.assignee_d, DivisionGroupType.VIEW_INCOMING_SHIPMENTS)
        u = self.assignee_u
        u.user.groups.add(g)
        shipmentassignment_post_save(
            ShipmentAssignment.__class__, self.target_d, True, False)
        self.assertTrue(
            u.user.has_perm('view_shipment', self.target_d.shipment))
        shipmentassignment_post_delete(
            ShipmentAssignment.__class__, self.target_d)
        # Test that user still has permission, if an existing
        # shipmentassignment exists
        self.assertTrue(
            u.user.has_perm('view_shipment', self.target_d.shipment))
        self.target_d.delete()
        self.assertFalse(
            u.user.has_perm('view_shipment', self.target_d.shipment))
