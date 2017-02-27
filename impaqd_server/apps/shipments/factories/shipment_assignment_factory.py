import factory
import factory.django
from faker import Faker
from django.db.models.signals import (
    pre_save, post_save, pre_delete, post_delete)
from .shipments import ShipmentFactory
from ..models.shipment_assignment import ShipmentAssignment

fake = Faker()


@factory.django.mute_signals(pre_save, post_save, pre_delete, post_delete)
class ShipmentAssignmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ShipmentAssignment

    shipment = factory.SubFactory(ShipmentFactory)
