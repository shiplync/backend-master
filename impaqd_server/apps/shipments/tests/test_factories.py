from django.test.testcases import TestCase
from django.core.exceptions import ValidationError

from ..factories.generic_user_factory import GenericUserFactory
from ..factories.generic_company_factory import UnknownCompanyFactory
from ..factories.user_factory import UserFactory
from ..models.generic_user import GenericUser


class UserFactoryTests(TestCase):
    def test_user_factory_sets_default_password(self):
        user = UserFactory()
        self.assertTrue(user.check_password('password'))

    def test_user_factory_sets_defined_password(self):
        user = UserFactory(password='other_password')
        self.assertTrue(user.check_password('other_password'))


class GenericCompanyFactoryTests(TestCase):
    @classmethod
    def setUpClass(cls):
        # call super, then add your code
        super(cls, GenericCompanyFactoryTests).setUpClass()

    @classmethod
    def tearDownClass(cls):
        # add your code first, then call super
        super(cls, GenericCompanyFactoryTests).tearDownClass()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_generic_company_factory_builds_valid_object(self):
        company = UnknownCompanyFactory()
        try:
            company.full_clean()
        except ValidationError as e:
            self.fail(e.message_dict)


class GenericUserFactoryTests(TestCase):
    @classmethod
    def setUpClass(cls):
        # call super, then add your code
        super(cls, GenericUserFactoryTests).setUpClass()

    @classmethod
    def tearDownClass(cls):
        # add your code first, then call super
        super(cls, GenericUserFactoryTests).tearDownClass()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_generic_user_builds_valid_object(self):
        user = GenericUserFactory()
        try:
            user.full_clean()
        except ValidationError as e:
            self.fail(e.message_dict)

    def test_generic_user_creates_user(self):
        user = GenericUserFactory.create()
        self.assertIsNotNone(user.user)
        self.assertIsNotNone(user.user.pk)

    def test_generic_user_get_by_user(self):
        user = GenericUserFactory.create()
        reuser = GenericUser.objects.get(user_id=user.user.pk)
        self.assertIsNotNone(reuser.user)
