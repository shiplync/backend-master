import factory
import factory.django
from faker import Faker
from django.db.models.signals import (
    pre_save, post_save, pre_delete, post_delete)
from ..models.user_invite import UserInvite
from .generic_company_factory import UnknownCompanyFactory

fake = Faker()


@factory.django.mute_signals(pre_save, post_save, pre_delete, post_delete)
class UserInviteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserInvite

    first_name = factory.LazyAttribute(lambda u: fake.first_name())
    last_name = factory.LazyAttribute(lambda u: fake.last_name())
    email = factory.LazyAttribute(lambda u: fake.email())
    company = factory.SubFactory(UnknownCompanyFactory)
