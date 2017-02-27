from django.db.models.signals import (
    pre_save, post_save, pre_delete,
    post_delete)

import random
import factory
import factory.django
from faker import Faker

from ..models.demo_account import DemoAccount

fake = Faker()


@factory.django.mute_signals(pre_save, post_save, pre_delete, post_delete)
class DemoAccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DemoAccount

    email = factory.LazyAttribute(lambda s: fake.email())
    password = factory.LazyAttribute(lambda s: fake.password())
    first_name = factory.LazyAttribute(lambda s: fake.first_name())
    last_name = factory.LazyAttribute(lambda s: fake.last_name())
    phone = factory.LazyAttribute(lambda s: fake.phone_number())
    company_name = factory.LazyAttribute(lambda s: fake.company())
    dot = factory.LazyAttribute(
        lambda s: random.randint(1000000, 9999999))
