import factory
import factory.django
from faker import Faker
from django.db.models.signals import (
    pre_save, post_save, pre_delete, post_delete)
from .user_factory import UserFactory
from .generic_company_factory import UnknownCompanyFactory
from .file_context_factory import FileContextFactory
from ..models import BasePermissionCollection, BasePermission

fake = Faker()


@factory.django.mute_signals(pre_save, post_save, pre_delete, post_delete)
class BasePermissionCollectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BasePermissionCollection


@factory.django.mute_signals(pre_save, post_save, pre_delete, post_delete)
class BasePermissionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BasePermission