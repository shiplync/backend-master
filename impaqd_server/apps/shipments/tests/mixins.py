from ..models.generic_user import generic_user_post_save, genericuser_pre_save
from ..utils import username_from_email
from faker import Faker
fake = Faker()


class GenericUserTestMixin(object):
    def test_update_user_fields_updates_email(self):
        self.generic_user.email = fake.email()
        self.assertNotEqual(
            self.generic_user.email,
            self.generic_user.user.email)
        generic_user_post_save(
            self.generic_user.__class__,
            self.generic_user, None, None)
        self.assertEqual(self.generic_user.email, self.generic_user.user.email)

    def test_update_user_fields_updates_user_username(self):
        self.generic_user.email = fake.email()
        pre_username = self.generic_user.user.username
        generic_user_post_save(
            self.generic_user.__class__, self.generic_user, None, None)
        post_username = self.generic_user.user.username
        self.assertNotEqual(pre_username, post_username)
        self.assertTrue(self.generic_user.email.startswith(post_username))

    def test_update_user_fields_trims_user_username(self):
        long_username = ''.join(fake.words(10))
        while len(long_username) < 30 or len(long_username) > 55:
            long_username = ''.join(fake.words(10))
        expected_username = long_username[:30]
        self.generic_user.email = '%s@example.com' % long_username
        generic_user_post_save(
            self.generic_user.__class__, self.generic_user, None, None)
        actual_username = self.generic_user.user.username
        self.assertEqual(expected_username, actual_username)

    def test_user_email_username_stays_lowercase(self):
        email_upper = fake.email().upper()
        self.generic_user.email = email_upper
        genericuser_pre_save(
            self.generic_user.__class__, self.generic_user, None)
        generic_user_post_save(
            self.generic_user.__class__, self.generic_user, None, None)
        self.assertEqual(
            self.generic_user.user.email, email_upper.lower())
        self.assertEqual(
            self.generic_user.user.username,
            username_from_email(email_upper.lower()))
