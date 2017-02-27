import factory
import factory.django
from faker import Faker
from django.utils import timezone
from django.db.models.signals import (
    pre_save, post_save, pre_delete, post_delete)

from .models import Subscription

fake = Faker()


@factory.django.mute_signals(pre_save, post_save, pre_delete, post_delete)
class SubscriptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Subscription

    payment_ready = True
    trial_length = 30
    trial_start = factory.LazyAttribute(lambda c: timezone.now())
