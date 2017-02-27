from django.test.testcases import TestCase
from ..factories.generic_user_factory import (
    TOSAcceptanceFactory, GenericUserFactory)
from ..models.generic_user import genericuser_pre_save
from ..models import TOSAcceptanceStatus


class TOSAcceptanceTests(TestCase):
    @classmethod
    def setUpClass(cls):
        # call super, then add your code
        super(cls, TOSAcceptanceTests).setUpClass()

    @classmethod
    def tearDownClass(cls):
        # add your code first, then call super
        super(cls, TOSAcceptanceTests).tearDownClass()

    def setUp(self):
        self.target = TOSAcceptanceFactory.create()
        self.generic_user = GenericUserFactory.create(
            tos_acceptance=self.target)
        pass

    def tearDown(self):
        pass

    def test_tos_acceptance_unicode_returns_user_email(self):
        self.assertIsNotNone(self.target.genericuser)
        self.assertEqual(self.target.genericuser.email, unicode(self.target))

    def test_tos_acceptance_unicode_returns_empty_string(self):
        self.generic_user.tos_acceptance = None
        self.assertEqual('', unicode(self.target))

    def test_tos_created_on_generic_user_pre_save(self):
        self.generic_user.tos_acceptance = None
        genericuser_pre_save(
            self.generic_user.__class__, self.generic_user, None)
        self.assertIsNotNone(self.generic_user.tos_acceptance)
        self.assertEqual(
            self.generic_user.tos_acceptance.tos_status,
            TOSAcceptanceStatus.UNSET)
