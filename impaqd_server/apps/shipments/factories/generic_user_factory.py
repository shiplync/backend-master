import re
import factory
from factory import post_generation
import factory.django
from faker import Faker
from django.db.models.signals import (
    pre_save, post_save, pre_delete, post_delete)
from .user_factory import UserFactory
from .generic_company_factory import UnknownCompanyFactory
from .file_context_factory import FileContextFactory
from ..models.tos_acceptance import TOSAcceptance
from ..models import GenericUser

from phonenumber_field.phonenumber import PhoneNumber
fake = Faker()


@factory.django.mute_signals(pre_save, post_save)
class TOSAcceptanceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TOSAcceptance
    tos_status = 1


@factory.django.mute_signals(pre_save, post_save, pre_delete, post_delete)
class GenericUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GenericUser

    company = factory.SubFactory(UnknownCompanyFactory)
    user = factory.SubFactory(UserFactory)
    email = factory.LazyAttribute(lambda g: g.user.email)
    first_name = factory.LazyAttribute(lambda g: g.user.first_name)
    last_name = factory.LazyAttribute(lambda g: g.user.last_name)
    # photo
    profile_photo = factory.SubFactory(FileContextFactory)
    tos_acceptance = factory.SubFactory(TOSAcceptanceFactory)
    # created_at
    # updated_at
    # permissions
    # last_location
    # last_location_timestamp
    # vehicle_type

    @post_generation
    def post(obj, create, extracted, **kwargs):
        # save obj and related objects
        obj.company.owner = obj
        obj.company.owner.user.save()
        obj.company.owner.profile_photo.save()
        obj.company.owner.tos_acceptance.save()
        obj.company.owner.save()
        obj.company.save()
