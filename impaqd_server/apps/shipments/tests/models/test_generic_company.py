import random

from django.test.testcases import TestCase
from django.contrib.auth.models import Group
from django.utils import timezone
from datetime import timedelta

from faker import Faker
fake = Faker()

from ...factories.generic_company_factory import UnknownCompanyFactory
from ...models.generic_company import (
    GenericCompany, genericcompany_post_save_create_groups,
    genericcompany_pre_save_create_subscription,
    genericcompany_post_delete_remove_groups, CompanyGroupType)
from ...factories.generic_user_factory import GenericUserFactory
from ...models.generic_user import (
    GenericUser, genericuser_post_save_set_groups, UserType)


class GenericCompanyTests(TestCase):
    @classmethod
    def setUpClass(cls):
        # call super, then add your code
        super(cls, GenericCompanyTests).setUpClass()

    @classmethod
    def tearDownClass(cls):
        # add your code first, then call super
        super(cls, GenericCompanyTests).tearDownClass()

    def setUp(self):
        self.target = UnknownCompanyFactory.create()
        self.groups = [
            CompanyGroupType.VIEW_INCOMING_SHIPMENTS % self.target.id,
            CompanyGroupType.MANAGERS % self.target.id,
            CompanyGroupType.ALL % self.target.id]

    def tearDown(self):
        pass

    def test_create_company_creates_groups(self):
        # Test that groups doesnt exist
        for g in self.groups:
            self.assertFalse(Group.objects.filter(name=g).count())
        # Create groups
        genericcompany_post_save_create_groups(
            GenericCompany.__class__, self.target, False, False)
        # Test that groups exist
        for g in self.groups:
            self.assertTrue(Group.objects.filter(name=g).count())

    def test_delete_company_removes_groups(self):
        # Create groups
        genericcompany_post_save_create_groups(
            GenericCompany.__class__, self.target, False, False)
        # Test that groups exist
        for g in self.groups:
            self.assertTrue(Group.objects.filter(name=g).count())
        # Delete groups
        genericcompany_post_delete_remove_groups(
            GenericCompany.__class__, self.target)
        # Test that groups doesnt exist
        for g in self.groups:
            self.assertFalse(Group.objects.filter(name=g).count())

    def test_unknown_user_set_company_groups(self):
        user_type = UserType.UNKNOWN
        genericuser = GenericUserFactory.create(user_type=user_type)
        user = genericuser.user
        self.assertTrue(user.groups.count() == 0)
        genericuser_post_save_set_groups(
            GenericUser, genericuser, False, False)
        # Expected one group
        self.assertTrue(user.groups.count() == 1)
        try:
            user.groups.get(name=CompanyGroupType.ALL % genericuser.company.pk)
            self.assertTrue(True)
        except Group.DoesNotExist:
            self.assertTrue(False)

    def test_representative_user_set_company_groups(self):
        user_type = random.choice(UserType.REPRESENTATIVES)
        genericuser = GenericUserFactory.create(user_type=user_type)
        user = genericuser.user
        self.assertTrue(
            user.groups.count() == 0)
        genericuser_post_save_set_groups(
            GenericUser, genericuser, False, False)
        # Expected one group
        self.assertTrue(user.groups.count() == 1)
        try:
            user.groups.get(name=CompanyGroupType.ALL % genericuser.company.pk)
            self.assertTrue(True)
        except Group.DoesNotExist:
            self.assertTrue(False)

    def test_supervisor_user_set_company_groups(self):
        user_type = random.choice(UserType.SUPERVISORS)
        genericuser = GenericUserFactory.create(user_type=user_type)
        user = genericuser.user
        self.assertTrue(
            user.groups.count() == 0)
        genericuser_post_save_set_groups(
            GenericUser, genericuser, False, False)
        # Expected one group
        self.assertTrue(user.groups.count() == 1)
        try:
            user.groups.get(name=CompanyGroupType.ALL % genericuser.company.pk)
            self.assertTrue(True)
        except Group.DoesNotExist:
            self.assertTrue(False)

    def test_manager_user_set_company_groups(self):
        user_type = random.choice(UserType.MANAGERS)
        genericuser = GenericUserFactory.create(user_type=user_type)
        user = genericuser.user
        self.assertTrue(
            user.groups.count() == 0)
        genericuser_post_save_set_groups(
            GenericUser, genericuser, False, False)
        # Expected three groups
        self.assertTrue(user.groups.count() == 3)
        try:
            user.groups.get(name=CompanyGroupType.ALL % genericuser.company.pk)
            user.groups.get(
                name=CompanyGroupType.MANAGERS % genericuser.company.pk)
            user.groups.get(
                name=CompanyGroupType.VIEW_INCOMING_SHIPMENTS %
                genericuser.company.pk)
            self.assertTrue(True)
        except Group.DoesNotExist:
            self.assertTrue(False)

    def test_company_subscription_trial_active(self):
        self.assertEqual(self.target.subscription.trial_length, 30)
        self.assertEqual(
            self.target.subscription.trial_start.date(),
            timezone.now().date())
        self.assertTrue(self.target.subscription.trial_active)
        # Test that trial becomes inactive
        self.target.subscription.trial_start = (
            self.target.subscription.trial_start - timedelta(
                days=(self.target.subscription.trial_length+1)))
        self.assertFalse(self.target.subscription.trial_active)
