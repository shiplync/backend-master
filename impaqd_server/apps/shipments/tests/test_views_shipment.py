import json
from rest_framework.test import APITestCase
from rest_framework.renderers import JSONRenderer
from ..factories.equipment_tag_factory import (
    EquipmentTagShipmentAssigneeFactory)
from ..factories.generic_user_factory import GenericUserFactory
from ..factories.shipments import ShipmentFactory
from ..models.generic_user import (
    GenericUser, UserType, genericuser_pre_save)
from ..models.shipments import Shipment
from ..serializers.shipments import ShipmentSerializer


clean_fields = [
    'created_at', 'updated_at', 'id', 'owner', 'owner_user', 'carrier',
    'carrier_driver', 'locations']


def clean_shipment(d):
    for k, v in d.iteritems():
        if k in clean_fields:
            del d[k]
        try:
            clean_shipment(v)
        except:
            pass
    return d


class ShipmentViewSetTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        # call super, then add your code
        super(cls, ShipmentViewSetTestCase).setUpClass()

    @classmethod
    def tearDownClass(cls):
        # call super, then add your code
        super(cls, ShipmentViewSetTestCase).tearDownClass()

    def setUp(self):
        self.shipment = ShipmentFactory()
        self.path = '/api/shipments/'
        self.shipper = GenericUserFactory(user_type=UserType.BROKER_MANAGER)
        # Set permissions
        self.shipper.save()
        genericuser_pre_save(GenericUser.__class__, self.shipper, False)

    def tearDown(self):
        pass

    def test_post_shipment_full(self):
        serializer = ShipmentSerializer(self.shipment)
        data = clean_shipment(serializer.data)
        self.client.force_authenticate(user=self.shipper.user)
        json_data = json.loads(JSONRenderer().render(data))
        response = self.client.post(self.path, json_data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_post_shipment_empty(self):
        self.client.force_authenticate(user=self.shipper.user)
        json_data = {}
        response = self.client.post(self.path, json_data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_patch_shipment_full(self):
        shipment_mock = ShipmentFactory(
            owner=self.shipper.company, owner_user=self.shipper)
        shipment_mock.save()
        shipment_target = ShipmentFactory(
            owner=self.shipper.company, owner_user=self.shipper)
        shipment_target.save()
        serializer = ShipmentSerializer(shipment_mock)
        data = clean_shipment(serializer.data).copy()
        self.client.force_authenticate(user=self.shipper.user)
        json_data = json.loads(JSONRenderer().render(data))
        path = '%s%i/' % (self.path, shipment_target.id)
        response = self.client.patch(
            path, json_data, format='json')
        self.assertEqual(response.status_code, 200)
        shipment_target = Shipment.objects.get(pk=shipment_target.id)
        res1 = json.loads(
            JSONRenderer().render(
                clean_shipment(ShipmentSerializer(shipment_mock).data)))
        # print res1
        res2 = json.loads(
            JSONRenderer().render(
                clean_shipment(ShipmentSerializer(shipment_target).data)))
        # print res2
        # TODO: compare res1 and res2

    def test_patch_shipment_empty(self):
        shipment_target = ShipmentFactory(
            owner=self.shipper.company, owner_user=self.shipper)
        shipment_target.save()
        self.client.force_authenticate(user=self.shipper.user)
        path = '%s%i/' % (self.path, shipment_target.id)
        response = self.client.patch(
            path, {}, format='json')
        self.assertEqual(response.status_code, 200)
