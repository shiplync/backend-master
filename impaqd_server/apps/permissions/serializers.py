from rest_framework import serializers
from .models import BasePermission, BasePermissionCollection


class BasePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasePermission
        fields = ('name', 'is_set', 'is_editable',)


class BasePermissionCollectionSerializer(serializers.ModelSerializer):
    # permissions = serializers.SlugRelatedField(many=True, slug_field='name')
    permissions = BasePermissionSerializer(many=True)

    class Meta:
        model = BasePermissionCollection
