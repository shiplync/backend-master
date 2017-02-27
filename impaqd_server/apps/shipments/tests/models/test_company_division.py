import random

from django.test.testcases import TestCase
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

from faker import Faker
fake = Faker()

from ...factories.company_division_factory import (
    CompanyDivisionFactory, CompanyDivisionMembershipFactory)
from ...factories.generic_user_factory import GenericUserFactory
from ...factories.generic_company_factory import UnknownCompanyFactory
from ...models.generic_user import UserType
from ...models.company_division import (
    CompanyDivision, DivisionGroupType, CompanyDivisionMembership,
    companydivision_post_save_create_groups,
    companydivision_post_delete_remove_groups,
    companydivisionmembership_post_save_set_groups,
    companydivisionmembership_post_delete_set_groups)


class CompanyDivisionTests(TestCase):
    @classmethod
    def setUpClass(cls):
        # call super, then add your code
        super(cls, CompanyDivisionTests).setUpClass()

    @classmethod
    def tearDownClass(cls):
        # add your code first, then call super
        super(cls, CompanyDivisionTests).tearDownClass()

    def setUp(self):
        self.target = CompanyDivisionFactory.create()
        self.genericuser = GenericUserFactory.create()
        self.user = self.genericuser.user
        self.membership = CompanyDivisionMembershipFactory(
            division=self.target, user=self.genericuser)
        self.groups = [
            DivisionGroupType.VIEW_INCOMING_SHIPMENTS % self.target.id,
            DivisionGroupType.SUPERVISORS % self.target.id,
            DivisionGroupType.ALL % self.target.id]

    def tearDown(self):
        pass

    def test_create_division_creates_groups(self):
        # Test that groups doesnt exist
        for g in self.groups:
            self.assertFalse(Group.objects.filter(name=g).count())
        # Create groups
        companydivision_post_save_create_groups(
            CompanyDivision.__class__, self.target, False, False)
        # Test that groups exist
        for g in self.groups:
            self.assertTrue(Group.objects.filter(name=g).count())

    def test_delete_division_removes_groups(self):
        # Create groups
        companydivision_post_save_create_groups(
            CompanyDivision.__class__, self.target, False, False)
        # Test that groups exist
        for g in self.groups:
            self.assertTrue(Group.objects.filter(name=g).count())
        # Delete groups
        companydivision_post_delete_remove_groups(
            CompanyDivision.__class__, self.target)
        # Test that groups doesnt exist
        for g in self.groups:
            self.assertFalse(Group.objects.filter(name=g).count())

    def test_unknown_user_set_division_groups(self):
        self.genericuser.user_type = UserType.UNKNOWN
        self.assertTrue(self.user.groups.count() == 0)
        companydivisionmembership_post_save_set_groups(
            CompanyDivisionMembership, self.membership, False, False)
        try:
            self.user.groups.get(
                name=DivisionGroupType.ALL % self.target.pk)
            self.assertTrue(True)
        except Group.DoesNotExist:
            self.assertTrue(False)

    def test_representative_user_set_company_groups(self):
        self.genericuser.user_type = random.choice(UserType.REPRESENTATIVES)
        self.assertTrue(self.user.groups.count() == 0)
        companydivisionmembership_post_save_set_groups(
            CompanyDivisionMembership, self.membership, False, False)
        try:
            self.user.groups.get(
                name=DivisionGroupType.ALL % self.target.pk)
            self.assertTrue(True)
        except Group.DoesNotExist:
            self.assertTrue(False)

    def test_supervisor_user_set_company_groups(self):
        self.genericuser.user_type = random.choice(UserType.SUPERVISORS)
        self.assertTrue(self.user.groups.count() == 0)
        companydivisionmembership_post_save_set_groups(
            CompanyDivisionMembership, self.membership, False, False)
        try:
            self.user.groups.get(
                name=DivisionGroupType.ALL % self.target.pk)
            self.user.groups.get(
                name=DivisionGroupType.SUPERVISORS
                % self.target.pk)
            self.user.groups.get(
                name=DivisionGroupType.VIEW_INCOMING_SHIPMENTS
                % self.target.pk)
            self.assertTrue(True)
        except Group.DoesNotExist:
            self.assertTrue(False)

    def test_manager_user_set_company_groups(self):
        self.genericuser.user_type = random.choice(UserType.MANAGERS)
        self.assertTrue(self.user.groups.count() == 0)
        companydivisionmembership_post_save_set_groups(
            CompanyDivisionMembership, self.membership, False, False)
        try:
            self.user.groups.get(
                name=DivisionGroupType.ALL % self.target.pk)
            self.user.groups.get(
                name=DivisionGroupType.SUPERVISORS
                % self.target.pk)
            self.user.groups.get(
                name=DivisionGroupType.VIEW_INCOMING_SHIPMENTS
                % self.target.pk)
            self.assertTrue(True)
        except Group.DoesNotExist:
            self.assertTrue(False)

    def test_delete_membership_removes_user_from_group(self):
        self.assertTrue(self.user.groups.count() == 0)
        companydivisionmembership_post_save_set_groups(
            CompanyDivisionMembership, self.membership, False, False)
        try:
            self.user.groups.get(
                name=DivisionGroupType.ALL % self.target.pk)
        except Group.DoesNotExist:
            self.assertTrue(False)
        self.membership.delete()
        # Check that group does not exist
        try:
            self.user.groups.get(
                name=DivisionGroupType.ALL % self.target.pk)
            self.assertTrue(False)
        except Group.DoesNotExist:
            self.assertTrue(True)

    def test_create_membership_fails_division_different_company(self):
        self.target.company = UnknownCompanyFactory()
        try:
            membership = CompanyDivisionMembership.objects.create(
                division=self.target, user=self.genericuser)
            membership.full_clean()
            self.assertTrue(False)
        except ValidationError:
            self.assertTrue(True)

    def test_create_membership_deletes_existing_membership(self):
        self.assertTrue(self.genericuser.companydivision_set.count() == 1)
        self.assertTrue(self.genericuser.division == self.target)
        division = CompanyDivisionFactory.create(
            company=self.genericuser.company)
        CompanyDivisionMembership.objects.create(
            division=division, user=self.genericuser)
        self.assertTrue(self.genericuser.companydivision_set.count() == 1)
        self.assertTrue(self.genericuser.division == division)
