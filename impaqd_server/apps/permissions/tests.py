from django.test import TestCase
import unittest

from impaqd_server.apps.shipments.models.generic_user import (
    UserType, generic_user_post_save, genericuser_pre_save,
    generic_user_pre_delete)
from impaqd_server.apps.shipments.factories import (
    GenericUserFactory)
from .models import base_permission_pre_delete
import random


class PermissionsCollectionTests(TestCase):
    @classmethod
    def setUpClass(cls):
        # call super, then add your code
        super(cls, PermissionsCollectionTests).setUpClass()

    @classmethod
    def tearDownClass(cls):
        # add your code first, then call super
        super(cls, PermissionsCollectionTests).tearDownClass()

    def setUp(self):
        self.user = GenericUserFactory.create(
            user_type=random.choice(UserType.VALID_TYPES))
        # self.permission_collection = PermissionCollectionFactory.create()

    def tearDown(self):
        pass

    def test_generic_user_has_permission_collection(self):
        self.assertIsNone(self.user.permissions)
        genericuser_pre_save(self.user.__class__, self.user, False)
        self.assertIsNotNone(self.user.permissions)
        self.assertEqual(self.user.permissions.user_type, self.user.user_type)

    def test_permission_collection_has_base_permissions(self):
        genericuser_pre_save(self.user.__class__, self.user, False)
        generic_user_post_save(self.user.__class__, self.user, True, False)
        self.assertTrue(self.user.permissions.permissions.count() > 0)

    @unittest.skip("pending")
    def test_deleting_permission_collection_deletes_base_permissions(self):
        genericuser_pre_save(self.user.__class__, self.user, False)
        generic_user_post_save(self.user.__class__, self.user, True, False)
        p = self.user.permissions.permissions.all()[0]
        self.assertIsNotNone(p)
        self.user.permissions.delete()
        generic_user_pre_delete(self.user.__class__, self.user)
        self.assertIsNone(p)


def BasePermissionTests(TestCase):
    @classmethod
    def setUpClass(cls):
        # call super, then add your code
        super(cls, BasePermissionTests).setUpClass()

    @classmethod
    def tearDownClass(cls):
        # add your code first, then call super
        super(cls, BasePermissionTests).tearDownClass()

    def setUp(self):
        self.user = GenericUserFactory.create()

    def tearDown(self):
        pass

    def test_create_base_permission_assigns_permission(self):
        genericuser_pre_save(self.user.__class__, self.user, False)
        generic_user_post_save(self.user.__class__, self.user, True, False)
        p = self.user.permissions.permissions.all()[0]
        codename = p.codename
        self.assertTrue(self.user.has_perm(codename))

    def test_delete_base_permission_removes_permission(self):
        genericuser_pre_save(self.user.__class__, self.user, False)
        generic_user_post_save(self.user.__class__, self.user, True, False)
        p = self.user.permissions.permissions.all()[0]
        codename = p.codename
        base_permission_pre_delete(p.__class__, p)
        self.assertFalse(self.user.has_perm(codename))
