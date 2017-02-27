import random
from django.test.testcases import TestCase
from django.utils import timezone
from impaqd_server.apps.shipments.factories.company_invite_factory import (
    CompanyInviteFactory)
from impaqd_server.apps.shipments.factories.generic_user_factory import (
    GenericUserFactory)
from impaqd_server.apps.shipments.models.relations import (
    CompanyInvite, company_invite_post_save, CompanyRelation)
from impaqd_server.apps.shipments.models.generic_user import (
    GenericUser, generic_user_post_save)
from impaqd_server.apps.shipments.models.generic_company import (
    GenericCompany, generic_company_post_save)
from impaqd_server.apps.shipments.tasks import (
    task_new_user_or_company_create_company_relations)


class CompanyInviteTests(TestCase):
    @classmethod
    def setUpClass(cls):
        # call super, then add your code
        super(cls, CompanyInviteTests).setUpClass()

    @classmethod
    def tearDownClass(cls):
        # add your code first, then call super
        super(cls, CompanyInviteTests).tearDownClass()

    def setUp(self):
        self.inviter_user = GenericUserFactory()
        self.inviter_user.save()
        self.inviter_company = self.inviter_user.company
        self.inviter_company.owner = self.inviter_user
        self.inviter_company.save()

        self.invitee_user = GenericUserFactory()
        self.invitee_user.save()
        self.invitee_company = self.invitee_user.company
        self.invitee_company.owner = self.invitee_user
        self.invitee_company.save()

        self.invite = CompanyInviteFactory(
            inviter_company=self.inviter_company,
            inviter_user=self.inviter_user)

    def tearDown(self):
        pass

    def test_create_company_invite_when_invitee_company_exist(self):
        self.assertFalse(
            self.invitee_company in self.inviter_company.relations.all())
        self.assertFalse(
            self.inviter_company in self.invitee_company.relations.all())
        dot = random.randint(111111, 999999)
        self.invite.invitee_dot = dot
        self.invite.save()
        self.invitee_company.dot = dot
        self.invitee_company.save()
        company_invite_post_save(
            CompanyInvite.__class__, self.invite, True, False)
        self.assertTrue(
            self.invitee_company in self.inviter_company.relations.all())
        self.assertTrue(
            self.inviter_company in self.invitee_company.relations.all())

    def test_create_company_invite_when_invitee_user_exist(self):
        self.assertFalse(
            self.invitee_company in self.inviter_company.relations.all())
        self.assertFalse(
            self.inviter_company in self.invitee_company.relations.all())
        self.invite.invitee_email = self.invitee_user.email
        self.invite.save()
        company_invite_post_save(
            CompanyInvite.__class__, self.invite, True, False)
        self.assertTrue(
            self.invitee_company in self.inviter_company.relations.all())
        self.assertTrue(
            self.inviter_company in self.invitee_company.relations.all())

    def test_create_company_when_when_invitee_company_is_created(self):
        inviter_relations_count = self.inviter_company.relations.count()
        dot = random.randint(111111, 999999)
        self.invite.invitee_dot = dot
        self.invite.save()
        self.invitee_company.created_at = timezone.now()
        self.invitee_company.dot = dot
        self.invitee_company.save()
        task_new_user_or_company_create_company_relations(
            self.invitee_company)
        self.assertTrue(
            self.invitee_company in self.inviter_company.relations.all())
        self.assertTrue(
            self.inviter_company in self.invitee_company.relations.all())
        self.assertTrue(
            self.inviter_company.relations.count() ==
            inviter_relations_count + 1)

    def test_create_company_relation_invitee_user_is_created(self):
        inviter_relations_count = self.inviter_company.relations.count()
        self.invite.invitee_email = self.invitee_user.email
        self.invite.save()
        task_new_user_or_company_create_company_relations(
            self.invitee_user)
        self.assertTrue(
            self.invitee_company in self.inviter_company.relations.all())
        self.assertTrue(
            self.inviter_company in self.invitee_company.relations.all())
        self.assertTrue(
            self.inviter_company.relations.count() ==
            inviter_relations_count + 1)
