from rest_framework import serializers
import users
import companies
from .common import update_object
from impaqd_server.apps.shipments.models import (
    GenericUser, GenericCompany)
from impaqd_server.apps.permissions.serializers import (
    BasePermissionCollectionSerializer)


class CarrierDriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenericUser

    def validate(self, data):
        # Make sure that another user doesn't exist if patching the email
        users.check_for_duplicate_user_on_patch(self, data)
        return data


class CarrierDriverSerializerNested(CarrierDriverSerializer):
    profile_photo = users.FileContextSerializer(required=False, read_only=True)
    company = companies.CarrierCompanySerializerNested()
    permissions = BasePermissionCollectionSerializer()

    def create(self, validated_data):
        return GenericUser.objects.create()

    def update(self, instance, validated_data):
        update_object(validated_data.pop('company'), instance.company)
        update_object(validated_data, instance)
        return instance


class CarrierVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenericCompany
        fields = ('id', 'verified')
