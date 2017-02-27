from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .common import update_object
from ..models import (
    ShipmentAssignment)
from ..models.shipment_assignment import (
    ShipmentCarrierAssignment, ShipmentDriverAssignment)
from ..models.generic_company import GenericCompany


class CustomContentTypeField(serializers.RelatedField):
    def to_representation(self, value):
        return value.model

    def to_internal_value(self, value):
        return ContentType.objects.get(model=value)


class ShipmentAssignmentSerializer(serializers.ModelSerializer):
    parent_content_type = CustomContentTypeField(read_only=True)
    assignee_content_type = CustomContentTypeField(
        read_only=False, queryset=ShipmentAssignment.objects.all())
    carrier_assignment = serializers.ReadOnlyField()
    driver_assignment = serializers.ReadOnlyField()

    class Meta:
        model = ShipmentAssignment
        read_only_fields = ('parent_id', 'parent_content_type', 'assigner')

    def validate(self, attrs):
        attrs.update(assigner=self.context['request'].user.genericuser)
        attrs.update(parent=self.context['request'].user.genericuser.company)
        ct = ContentType.objects.get_for_model(GenericCompany)
        attrs.update(parent_content_type=ct)
        instance = ShipmentAssignment(**attrs)
        instance.clean()
        return attrs


class ShipmentCarrierAssignmentSerializer(serializers.ModelSerializer):
    assignment = ShipmentAssignmentSerializer()

    class Meta:
        model = ShipmentCarrierAssignment

    def create(self, validated_data):
        assignment = ShipmentAssignment.objects.create(
            **validated_data.pop('assignment', {}))
        return ShipmentCarrierAssignment.objects.create(
            assignment=assignment)

    def update(self, instance, validated_data):
        update_object(
            validated_data.pop('assignment', {}),
            instance.assignment)
        update_object(validated_data, instance)
        return instance


class ShipmentDriverAssignmentSerializer(serializers.ModelSerializer):
    assignment = ShipmentAssignmentSerializer()

    class Meta:
        model = ShipmentDriverAssignment

    def create(self, validated_data):
        assignment = ShipmentAssignment.objects.create(
            **validated_data.pop('assignment', {}))
        return ShipmentDriverAssignment.objects.create(
            assignment=assignment)

    def update(self, instance, validated_data):
        update_object(
            validated_data.pop('assignment', {}),
            instance.assignment)
        update_object(validated_data, instance)
        return instance

    def validate(self, attrs):
        attrs_clean = attrs.copy()
        sa = ShipmentAssignment(attrs_clean.get('assignment'))
        attrs_clean.update(assignment=sa)
        instance = ShipmentDriverAssignment(**attrs_clean)
        instance.clean()
        return attrs
