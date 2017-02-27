import random
import factory
import factory.django
from faker import Faker
from django.db.models.signals import (
    pre_save, post_save, pre_delete, post_delete)
from .shipments import ShipmentFactory
from .generic_user_factory import GenericUserFactory
from ..models.equipment_tag import EquipmentTag, TagType, TagCategory

fake = Faker()


@factory.django.mute_signals(pre_save, post_save, pre_delete, post_delete)
class EquipmentTagShipmentAssigneeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EquipmentTag

    assigner = factory.SubFactory(GenericUserFactory)
    assignee = factory.SubFactory(ShipmentFactory)
    tag_type = factory.LazyAttribute(
        lambda i: random.choice(TagType.TAG_TYPE_CHOICES)[0])
    tag_category = factory.LazyAttribute(
        lambda i: random.choice(TagCategory.TAG_CATEGORY_CHOICES)[0])
