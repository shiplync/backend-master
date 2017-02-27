from django.test import TestCase, RequestFactory

from django.contrib.auth.models import User
from impaqd_server.apps.shipments.views.users import UsersListView
from ..factories import UserFactory

# Create your tests here.


class UsersListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        # call super, then add your code
        super(cls, UsersListViewTestCase).setUpClass()

    @classmethod
    def tearDownClass(cls):
        # call super, then add your code
        super(cls, UsersListViewTestCase).tearDownClass()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_head_returns_400_by_default(self):
        request = RequestFactory().head('/api/users/')
        view = UsersListView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 400)

    def test_head_returns_404_for_unknown_user_email(self):
        user = UserFactory.build()
        email = user.email
        self.assertFalse(User.objects.filter(email=email).exists())

        path = '/api/users?email=%s' % (email)
        request = RequestFactory().head(path)
        view = UsersListView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 404)

    def test_head_return_204_for_known_user_email(self):
        user = UserFactory.create()
        email = user.email
        self.assertTrue(User.objects.filter(email=email).exists())

        path = '/api/users/?email=%s' % (email)
        request = RequestFactory().head(path)
        view = UsersListView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 204)
