from rest_framework.test import APITestCase
from guardian.shortcuts import assign_perm
from ..factories.equipment_tag_factory import (
    EquipmentTagShipmentAssigneeFactory)
from ..factories.generic_user_factory import GenericUserFactory
from ..factories.shipments import ShipmentFactory


class EquipmentTypeViewSetTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        # call super, then add your code
        super(cls, EquipmentTypeViewSetTestCase).setUpClass()

    @classmethod
    def tearDownClass(cls):
        # call super, then add your code
        super(cls, EquipmentTypeViewSetTestCase).tearDownClass()

    def setUp(self):
        self.mock = EquipmentTagShipmentAssigneeFactory()
        self.shipment = ShipmentFactory()
        self.assigner = GenericUserFactory()
        self.path = '/api/equipmenttags/'

    def tearDown(self):
        pass

    def test_post_equipmenttype(self):
        data = {'assignee_id': self.shipment.id, 'assignee_content_type':
                'shipment', 'tag_type': self.mock.tag_type, 'category':
                self.mock.tag_category}
        assign_perm('change_shipment', self.assigner.user, self.shipment)
        self.client.force_authenticate(user=self.assigner.user)
        response = self.client.post(self.path, data, format='json')
        self.assertEqual(
            response.data.get('assignee_id'), self.shipment.id)
