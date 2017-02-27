from django.test.testcases import TestCase

from django.core.exceptions import ValidationError

from faker import Faker
fake = Faker()

from ...factories.file_context_factory import FileContextFactory
from ...models.file_context import FileContext


class FileContextTests(TestCase):
    @classmethod
    def setUpClass(cls):
        # call super, then add your code
        super(cls, FileContextTests).setUpClass()

    @classmethod
    def tearDownClass(cls):
        # add your code first, then call super
        super(cls, FileContextTests).tearDownClass()

    def setUp(self):
        self.target = FileContextFactory.build()
        pass

    def tearDown(self):
        pass

    def test_file_context_valid(self):
        try:
            self.target.full_clean()
            self.assertTrue(True)
        except ValidationError as e:
            print e.message_dict
            self.fail("Failed Validation")
