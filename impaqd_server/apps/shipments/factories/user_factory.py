import factory
import factory.django
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import User
from faker import Faker

fake = Faker()


@factory.django.mute_signals(pre_save, post_save)
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.LazyAttribute(lambda u: fake.first_name())
    last_name = factory.LazyAttribute(lambda u: fake.last_name())
    username = factory.LazyAttribute(lambda u: '.'.join([u.first_name, u.last_name]))
    email = factory.LazyAttribute(lambda u: '%s@example.com' % u.username)
    password = factory.PostGenerationMethodCall('set_password', 'password')
    is_staff = False
    is_active = True
    is_superuser = False
