from django.test.testcases import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from ...factories.generic_user_factory import GenericUserFactory
from ...factories.user_invite_factory import UserInviteFactory
from ...models.user_invite import UserInvite
from ....notifications.models.user_invite import UserInviteNotif

from faker import Faker


class UserInviteTests(TestCase):
    @classmethod
    def setUpClass(cls):
        # call super, then add your code
        super(cls, UserInviteTests).setUpClass()

    @classmethod
    def tearDownClass(cls):
        # add your code first, then call super
        super(cls, UserInviteTests).tearDownClass()

    def setUp(self):
        assigner_user = GenericUserFactory()
        company = assigner_user.company
        self.invite = UserInviteFactory(
            assigner_user=assigner_user, company=company)

    def tearDown(self):
        pass

    def test_create_invite_sets_token(self):
        self.assertTrue(
            len(str(self.invite.token)) > 10)

    def test_delete_user_deletes_invite(self):
        self.invite.user = GenericUserFactory()
        self.assertIsNotNone(self.invite.user)
        self.invite.user.delete()
        try:
            self.invite.refresh_from_db()
        except UserInvite.DoesNotExist:
            self.assertTrue(True)
            return
        self.assertTrue(False)

    def test_create_invite_succeeds_with_remaining_user_invites(self):
        user = GenericUserFactory()
        user.company.subscription.no_users = 2
        user.company.subscription.no_trucks = 0
        UserInvite.objects.create(
            company=user.company, email=Faker().email())
        self.assertTrue(True)

    def test_create_invite_fails_without_remaining_user_invites(self):
        user = GenericUserFactory()
        user.company.subscription.no_users = 1
        user.company.subscription.no_trucks = 0
        try:
            i = UserInvite.objects.create(
                company=user.company, email=Faker().email())
            i.full_clean()
        except ValidationError:
            self.assertTrue(True)
            return
        self.assertTrue(False)

    def test_create_invite_fails_user_email_exists(self):
        existing_user = GenericUserFactory()
        existing_user.save()
        user = GenericUserFactory()
        try:
            i = UserInvite.objects.create(
                email=existing_user.email,
                company=user.company)
            i.full_clean()
        except ValidationError:
            self.assertTrue(True)
            return
        self.assertTrue(False)

    def test_create_invite_fails_invite_email_exists(self):
        user = GenericUserFactory()
        try:
            UserInvite.objects.create(
                email=self.invite.email,
                company=user.company)
        except IntegrityError:
            self.assertTrue(True)
            return
        self.assertTrue(False)

    def test_create_invite_sends_email(self):
        email = Faker().email()
        UserInvite.objects.create(
            email=email, company=self.invite.company)
        try:
            UserInviteNotif.objects.get(receiver_email=email)
            self.assertTrue(True)
        except UserInviteNotif.DoesNotExist:
            self.assertTrue(False)

    def test_create_invite_decrements_remaining_user_invites(self):
        self.invite.company.subscription.no_users = 100
        self.invite.company.subscription.no_trucks = 0
        rem = self.invite.company.remaining_user_invites
        # Check that company has one user and one userinvite
        self.assertEqual(rem, 98)
        UserInvite.objects.create(
            email=Faker().email(),
            company=self.invite.company)
        self.assertEqual(self.invite.company.remaining_user_invites, rem-1)

    def test_delete_invite_increments_remaining_user_invites(self):
        rem = self.invite.company.remaining_user_invites
        self.invite.delete()
        self.assertEqual(self.invite.company.remaining_user_invites, rem+1)
