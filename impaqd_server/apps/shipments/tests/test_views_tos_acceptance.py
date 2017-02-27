import unittest
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from ..models import TOSAcceptanceStatus, GlobalSettings
from ..views.tos_acceptance import TOSAcceptanceView
from ..factories.generic_user_factory import (
    TOSAcceptanceFactory, GenericUserFactory)


class TOSAcceptanceViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        # call super, then add your code
        super(cls, TOSAcceptanceViewTestCase).setUpClass()

    @classmethod
    def tearDownClass(cls):
        # call super, then add your code
        super(cls, TOSAcceptanceViewTestCase).tearDownClass()

    def setUp(self):
        self.settings = GlobalSettings.objects.create()
        self.tos = TOSAcceptanceFactory.create(
            tos_version=self.settings.current_tos_version)
        self.generic_user = GenericUserFactory.create(
            tos_acceptance=self.tos)
        self.factory = APIRequestFactory()
        self.path = '/api/tos/'

    def tearDown(self):
        pass

    @unittest.expectedFailure
    def test_tos_acceptance_view_returns_tos_status_unset_after_incrementing_tos_version(self):
        # GlobalSettings wont update in tests
        self.tos.tos_status = TOSAcceptanceStatus.ACCEPTED
        settings = GlobalSettings.objects.get()
        settings.current_tos_version = self.settings.current_tos_version + 1
        settings.save()
        settings = GlobalSettings.objects.get()
        request = self.factory.get(self.path, format='json')
        force_authenticate(request, user=self.generic_user.user)
        view = TOSAcceptanceView.as_view()
        response = view(request)
        self.assertEqual(
            response.data.get('tos_status'),
            TOSAcceptanceStatus.UNSET)

    def test_tos_acceptance_view_sets_tos_status_accepted_after_post(self):
        self.tos.tos_status = TOSAcceptanceStatus.UNSET
        request = self.factory.post(self.path, {}, format='json')
        force_authenticate(request, user=self.generic_user.user)
        view = TOSAcceptanceView.as_view()
        view(request)
        self.assertEqual(
            self.tos.tos_status,
            TOSAcceptanceStatus.ACCEPTED)
