import random
import factory
import factory.django
from faker import Faker
from django.db.models.signals import (
    pre_save, post_save, pre_delete, post_delete)
from .generic_company_factory import UnknownCompanyFactory
from ..models.company_division import (
    CompanyDivision, CompanyDivisionMembership)

fake = Faker()


@factory.django.mute_signals(pre_save, post_save, pre_delete, post_delete)
class CompanyDivisionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CompanyDivision

    company = factory.SubFactory(UnknownCompanyFactory)
    name = factory.LazyAttribute(lambda a: str(random.randint(1, 100000)))


@factory.django.mute_signals(pre_save, post_save, pre_delete, post_delete)
class CompanyDivisionMembershipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CompanyDivisionMembership
