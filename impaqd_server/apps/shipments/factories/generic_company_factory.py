import factory
import factory.django
from faker import Faker
from django.db.models.signals import (
    pre_save, post_save, pre_delete, post_delete)
from ..models.generic_company import GenericCompany, CompanyType
from ...payments.factories import SubscriptionFactory

fake = Faker()


@factory.django.mute_signals(pre_save, post_save, pre_delete, post_delete)
class UnknownCompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GenericCompany

    company_name = factory.LazyAttribute(lambda c: fake.company())
    insurance = None
    verified = True
    rejected = False
    owner = None  # set in test
    company_type = CompanyType.UNKNOWN
    registration_complete = True
    subscription = factory.SubFactory(SubscriptionFactory)
