import unittest
from django.test.testcases import TestCase

from django.core.exceptions import ValidationError

from faker import Faker
fake = Faker()

from ...factories.generic_user_factory import GenericUserFactory
from ...models.generic_user import GenericUser, genericuser_post_save_set_groups
# from ...models.generics import GenericUser


class GenericUserTests(TestCase):
    @classmethod
    def setUpClass(cls):
        # call super, then add your code
        super(cls, GenericUserTests).setUpClass()

    @classmethod
    def tearDownClass(cls):
        # add your code first, then call super
        super(cls, GenericUserTests).tearDownClass()

    def setUp(self):
        self.target = GenericUserFactory.create()
        pass

    def tearDown(self):
        pass

    def test_generic_user_valid(self):
        try:
            self.target.full_clean()
            self.assertTrue(True)
        except ValidationError as e:
            print e.message_dict
            self.fail("Failed Validation")

    def test_generic_user_unicode(self):
        self.assertEqual(self.target.email, unicode(self.target))

    def test_generic_user_name(self):
        self.assertIsNotNone(self.target.first_name)
        self.assertIsNotNone(self.target.last_name)
        first_name = self.target.first_name
        last_name = self.target.last_name
        self.assertEqual(self.target.name, "%s %s" % (first_name, last_name))

    def test_generic_user_name_if_no_first_name(self):
        self.assertIsNotNone(self.target.last_name)
        self.target.first_name = None
        self.assertEqual(self.target.name, self.target.email)

    def test_generic_user_name_if_no_last_name(self):
        self.assertIsNotNone(self.target.first_name)
        self.target.last_name = None
        self.assertEqual(self.target.name, self.target.first_name)

    def test_generic_user_name_if_first_name_empty(self):
        self.assertIsNotNone(self.target.last_name)
        self.target.first_name = ''
        self.assertEqual(self.target.name, self.target.email)

    @unittest.expectedFailure
    def test_generic_user_name_if_first_name_blank(self):
        self.assertIsNotNone(self.target.last_name)
        self.target.first_name = ' '
        self.assertEqual(self.target.name, ' ')
