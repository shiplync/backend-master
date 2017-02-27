from django.test.testcases import TestCase
from django.core import exceptions
from django.contrib.contenttypes.models import ContentType
from guardian.shortcuts import assign_perm
from impaqd_server.apps.shipments.factories.equipment_tag_factory import (
    EquipmentTagShipmentAssigneeFactory)


class EquipmentTagTests(TestCase):
    @classmethod
    def setUpClass(cls):
        # call super, then add your code
        super(cls, EquipmentTagTests).setUpClass()

    @classmethod
    def tearDownClass(cls):
        # add your code first, then call super
        super(cls, EquipmentTagTests).tearDownClass()

    def setUp(self):
        self.target = EquipmentTagShipmentAssigneeFactory()

    def tearDown(self):
        pass

    def test_assign_equipment_tag_shipment_assigner_missing_permission(self):
        try:
            self.target.full_clean()
            self.fail()
        except exceptions.ValidationError:
            self.assertTrue(True)

    def test_assign_equipment_tag_shipment(self):
        ct = ContentType.objects.get(model=self.target.assignee_content_type)
        codename = 'change_%s' % ct.model
        assign_perm(codename, self.target.assigner.user, self.target.assignee)
        try:
            self.target.full_clean()
            self.assertTrue(True)
        except exceptions.ValidationError:
            self.fail()
