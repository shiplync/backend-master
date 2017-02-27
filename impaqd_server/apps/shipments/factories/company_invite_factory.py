import factory
import factory.django
from faker import Faker
from django.db.models.signals import (
    pre_save, post_save, pre_delete, post_delete)
from ..models.relations import CompanyInvite

fake = Faker()


@factory.django.mute_signals(pre_save, post_save, pre_delete, post_delete)
class CompanyInviteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CompanyInvite
