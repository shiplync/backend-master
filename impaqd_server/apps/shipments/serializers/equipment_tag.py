from ..models.equipment_tag import EquipmentTag
from rest_framework import serializers
from rest_framework.fields import CharField
from django.contrib.contenttypes.models import ContentType


class CustomContentTypeField(serializers.RelatedField):
    def to_representation(self, value):
        return value.model

    def to_internal_value(self, value):
        return ContentType.objects.get(model=value)


class EquipmentTagSerializer(serializers.ModelSerializer):
    assignee_content_type = CustomContentTypeField(
        read_only=False, queryset=EquipmentTag.objects.all())
    tag_category_label = CharField(read_only=True)
    tag_type_label = CharField(read_only=True)

    class Meta:
        model = EquipmentTag
        exclude = ('assigner',)

    def validate(self, attrs):
        # Set assigner since it is excluded
        attrs.update(assigner=self.context['request'].user.genericuser)
        instance = EquipmentTag(**attrs)
        instance.clean()
        return attrs
