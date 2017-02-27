import unittest
from django.test.testcases import TestCase
from ..factories.generic_user_factory import (
    TOSAcceptanceFactory, GenericUserFactory)
from ..models import TOSAcceptanceStatus
from ..serializers import TOSAcceptanceSerializer


class TOSAcceptanceSerializerTests(TestCase):
    @classmethod
    def setUpClass(cls):
        # call super, then add your code
        super(cls, TOSAcceptanceSerializerTests).setUpClass()

    @classmethod
    def tearDownClass(cls):
        # add your code first, then call super
        super(cls, TOSAcceptanceSerializerTests).tearDownClass()

    def setUp(self):
        self.tos = TOSAcceptanceFactory.create()
        self.generic_user = GenericUserFactory.create(
            tos_acceptance=self.tos)
        self.target = TOSAcceptanceSerializer(self.tos)

    def tearDown(self):
        pass

    @unittest.expectedFailure
    def test_tos_is_unset_after_incrementing_tos_version(self):
        # TODO: Fix broken test
        self.tos.tos_status = TOSAcceptanceStatus.ACCEPTED
        self.assertTrue('tos_status' in self.target.data)
        self.target.data.pop('tos_status')
        self.assertFalse(self.target.data)
