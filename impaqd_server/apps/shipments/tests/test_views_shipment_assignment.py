from rest_framework.test import APITestCase
from guardian.shortcuts import assign_perm
from ..models.shipment_assignment import (
    ShipmentAssignment, shipmentassignment_post_save)
from ..factories.generic_user_factory import GenericUserFactory
from ..factories.shipments import ShipmentFactory
from ..factories.shipment_assignment_factory import ShipmentAssignmentFactory
from ..factories.company_division_factory import CompanyDivisionFactory


class ShipmentAssignmentViewSetTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        # call super, then add your code
        super(cls, ShipmentAssignmentViewSetTestCase).setUpClass()

    @classmethod
    def tearDownClass(cls):
        # call super, then add your code
        super(cls, ShipmentAssignmentViewSetTestCase).tearDownClass()

    def setUp(self):
        self.path = '/api/shipmentassignments/'

    def tearDown(self):
        pass

    def test_set_parent_when_shipment_assignment_found_with_assignee_user(self):
        # Test that target ShipmentAssignment's parent gets set to another
        # ShipmentAssignment (when parent's assignee is a company)
        grandparent = GenericUserFactory()
        parent = GenericUserFactory()
        target = GenericUserFactory()

        a1 = ShipmentAssignmentFactory(
            parent=grandparent.company, assignee=parent.company, r=True,
            can_delegate=True)
        shipmentassignment_post_save(
            ShipmentAssignment.__class__, a1, True, False)
        data = {'assignee_id': target.company.id, 'assignee_content_type':
                'genericcompany', 'shipment': a1.shipment.id}
        assign_perm('view_shipment', parent.user, a1.shipment)
        self.client.force_authenticate(user=parent.user)
        response = self.client.post(self.path, data, format='json')
        self.assertEqual(
            response.data.get('parent_content_type'), 'shipmentassignment')
        self.assertEqual(response.data.get('parent_id'), a1.id)
        self.assertEqual(
            response.data.get('assigner'), parent.id)

    def test_set_parent_when_shipment_assignment_found_with_assignee_division(self):
        # Test that ShipmentAssignment's parent gets set to another
        # ShipmentAssignment (when parent's assignee is a user)
        grandparent = GenericUserFactory()
        parent = GenericUserFactory()

        a1 = ShipmentAssignmentFactory(
            parent=grandparent.company, assignee=parent, r=True,
            can_delegate=True)
        shipmentassignment_post_save(
            ShipmentAssignment.__class__, a1, True, False)
        division = CompanyDivisionFactory.create()
        data = {'assignee_id': division.id, 'assignee_content_type':
                'companydivision', 'shipment': a1.shipment.id}
        assign_perm('view_shipment', parent.user, a1.shipment)
        self.client.force_authenticate(user=parent.user)
        response = self.client.post(self.path, data, format='json')
        self.assertEqual(
            response.data.get('parent_content_type'), 'shipmentassignment')
        self.assertEqual(response.data.get('parent_id'), a1.id)
        self.assertEqual(
            response.data.get('assigner'), parent.id)

    def test_set_parent_when_shipment_assignment_found_with_assignee_company(self):
        # Test that ShipmentAssignment's parent gets set to another
        # ShipmentAssignment (when parent's assignee is a user)
        grandparent = GenericUserFactory()
        parent = GenericUserFactory()
        target = GenericUserFactory()

        a1 = ShipmentAssignmentFactory(
            parent=grandparent.company, assignee=parent, r=True,
            can_delegate=True)
        shipmentassignment_post_save(
            ShipmentAssignment.__class__, a1, True, False)
        data = {'assignee_id': target.company.id, 'assignee_content_type':
                'genericcompany', 'shipment': a1.shipment.id}
        assign_perm('view_shipment', parent.user, a1.shipment)
        self.client.force_authenticate(user=parent.user)
        response = self.client.post(self.path, data, format='json')
        self.assertEqual(
            response.data.get('parent_content_type'), 'shipmentassignment')
        self.assertEqual(response.data.get('parent_id'), a1.id)
        self.assertEqual(
            response.data.get('assigner'), parent.id)

    def test_set_parent_company_when_no_shipment_assignment_found(self):
        # Test that ShipmentAssignment's parent gets set to parents company,
        # when there is no matiching ShipmentAssignment
        parent = GenericUserFactory()
        target = GenericUserFactory()
        s = ShipmentFactory()

        data = {'assignee_id': target.company.id, 'assignee_content_type':
                'genericcompany', 'shipment': s.id}
        assign_perm('view_shipment', parent.user, s)
        self.client.force_authenticate(user=parent.user)
        response = self.client.post(self.path, data, format='json')
        self.assertEqual(
            response.data.get('parent_content_type'), 'genericcompany')
        self.assertEqual(response.data.get('parent_id'), parent.company.id)
        self.assertEqual(
            response.data.get('assigner'), parent.id)
