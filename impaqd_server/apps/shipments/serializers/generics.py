from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from guardian.core import ObjectPermissionChecker

import users
from .company_division import CompanyDivisionSerializer
from .shipment_assignment import ShipmentAssignmentSerializer
from ..models import GenericUser, GenericCompany
from ..models.generic_user import UserType
from ..models.generic_company import (
    CompanyType, CompanyGroupType, get_company_group)
from ..models.company_division import CompanyDivision
from ..models.shipments import Shipment
from ..models.shipment_assignment import ShipmentAssignment


def get_shipment_assignment(context, obj, ct):
    # Optional: Check if user (obj) is assigned to shipment (kwarg) by
    # assigner (request.user) via a shipment assignment.
    # Set 'show_shipment_assignment' equal to shipment.pk
    # Returns: shipmentassignment.pk or false
    shipment_id_str = context.get('request')._request.GET.get(
        'show_shipment_assignment', None)
    if shipment_id_str:
        try:
            shipment_id = int(shipment_id_str)
            shipment = Shipment.objects.get(pk=shipment_id)
            s = ShipmentAssignment.objects.get(
                assigner=context.get('request').user.genericuser,
                assignee_content_type=ct, assignee_id=obj.id,
                shipment=shipment)
            return ShipmentAssignmentSerializer(s).data
        except Exception:
            return False
    pass


class CompanyTypeSerializer(serializers.BaseSerializer):
    def to_representation(self, val):
        status = filter(
            lambda x: x[0] == val, CompanyType.CHOICES)[0]
        return {
            'value': status[0],
            'label': status[1]
        }

    def to_internal_value(self, data):
        result = data
        if isinstance(data, dict) and 'value' in data:
            result = data['value']
        # Validate it is a valid choice
        if len(filter(lambda x: x[0] == result, CompanyType.CHOICES)):
            return result
        else:
            raise serializers.ValidationError('Not a valid company type')


class GenericCompanySerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(min_length=1, max_length=200)
    city = serializers.CharField(min_length=1, max_length=50)
    state = serializers.CharField(min_length=2, max_length=2)
    company_type = CompanyTypeSerializer(read_only=True)
    logo = users.FileContextSerializer(required=False, read_only=True)

    class Meta:
        model = GenericCompany
        exclude = ('owner',)
        read_only_fields = ('company_type',)


class GenericCompanyTeamSerializer(serializers.ModelSerializer):
    company_type = CompanyTypeSerializer(read_only=True)
    logo = serializers.SerializerMethodField()
    shipment_access = serializers.SerializerMethodField()
    shipment_assignment = serializers.SerializerMethodField()

    class Meta:
        model = GenericCompany
        fields = (
            'id', 'company_name', 'dot', 'company_type', 'logo',
            'shipment_access', 'shipment_assignment',)

    def get_shipment_access(self, obj):
        # Optional: Check if company (obj) has read access to shipment (kwarg).
        # Set 'show_shipment_access' equal to shipment.pk
        # Returns: true or false
        shipment_id_str = self.context.get('request')._request.GET.get(
            'show_shipment_access', None)
        if shipment_id_str:
            try:
                shipment_id = int(shipment_id_str)
                shipment = Shipment.objects.get(pk=shipment_id)
                ct = ContentType.objects.get_for_model(Shipment)
                perm = 'view_%s' % str(ct)
                group = get_company_group(
                    obj, CompanyGroupType.VIEW_INCOMING_SHIPMENTS)
                checker = ObjectPermissionChecker(group)
                return checker.has_perm(perm, shipment)
            except Exception:
                return False

    def get_shipment_assignment(self, obj):
        ct = ContentType.objects.get_for_model(GenericCompany)
        return get_shipment_assignment(self.context, obj, ct)

    def get_logo(self, obj):
        if obj.logo and self.context.get('request')._request.GET.get(
                'show_logo', None):
            return users.FileContextSerializer(obj.logo).data
        return None


class UserTypeSerializer(serializers.BaseSerializer):
    def to_representation(self, val):
        status = filter(
            lambda x: x[0] == val, UserType.CHOICES)[0]
        return {
            'value': status[0],
            'label': status[1],
            'is_manager': val in UserType.MANAGERS,
            'is_supervisor': val in UserType.SUPERVISORS,
            'is_representative': val in UserType.REPRESENTATIVES
        }

    def to_internal_value(self, data):
        result = data
        if isinstance(data, dict) and 'value' in data:
            result = data['value']
        # Validate it is a valid choice
        if len(filter(lambda x: x[0] == result, UserType.CHOICES)):
            return result
        else:
            raise serializers.ValidationError('Not a valid user type')


class GenericUserSerializer(serializers.ModelSerializer):
    user_type = UserTypeSerializer(required=True)
    company = GenericCompanySerializer(required=False, read_only=True)
    profile_photo = users.FileContextSerializer(required=False, read_only=True)
    name = serializers.ReadOnlyField()

    class Meta:
        model = GenericUser
        exclude = ('inactive',)

    def validate(self, data):
        # Make sure that another user doesn't exist if patching the email
        users.check_for_duplicate_user_on_patch(self, data)
        return data


class GenericUserTeamSerializer(serializers.ModelSerializer):
    user_type = UserTypeSerializer(required=True)
    profile_photo = serializers.SerializerMethodField()
    name = serializers.ReadOnlyField()
    division = CompanyDivisionSerializer()
    division_membership = serializers.SerializerMethodField()
    shipment_access = serializers.SerializerMethodField()
    shipment_assignment = serializers.SerializerMethodField()

    class Meta:
        model = GenericUser
        read_only_fields = ('division',)

    def validate(self, data):
        # Make sure that another user doesn't exist if patching the email
        users.check_for_duplicate_user_on_patch(self, data)
        return data

    def get_profile_photo(self, obj):
        if obj.profile_photo and self.context.get('request')._request.GET.get(
                'show_profile_photo', None):
            return users.FileContextSerializer(obj.profile_photo).data
        return None

    def get_shipment_access(self, obj):
        # Optional: Check if user (obj) has read access to shipment (kwarg).
        # Set 'show_shipment_access' equal to shipment.pk
        # Returns: true or false
        shipment_id_str = self.context.get('request')._request.GET.get(
            'show_shipment_access', None)
        if shipment_id_str:
            try:
                shipment_id = int(shipment_id_str)
                shipment = Shipment.objects.get(pk=shipment_id)
                ct = ContentType.objects.get_for_model(Shipment)
                perm = 'view_%s' % str(ct)
                return obj.user.has_perm(perm, shipment)
            except Exception:
                return False

    def get_shipment_assignment(self, obj):
        ct = ContentType.objects.get_for_model(GenericUser)
        return get_shipment_assignment(self.context, obj, ct)

    def get_division_membership(self, obj):
        # Optional: Check if user (obj) is a member a division (kwarg).
        # Set 'show_division_membership' equal to companydivision.pk
        # Returns: companydivisionmembership.pk or false
        member_id_str = self.context.get('request')._request.GET.get(
            'show_division_membership', None)
        if member_id_str:
            try:
                member_id = int(member_id_str)
                division = CompanyDivision.objects.get(pk=member_id)
                return division.companydivisionmembership_set.get(
                    user=obj.pk).pk
            except Exception:
                return False
