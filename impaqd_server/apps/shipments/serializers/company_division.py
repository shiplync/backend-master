from rest_framework import serializers

from ..models.company_division import (
    CompanyDivision, CompanyDivisionMembership)
from ..models.generic_user import GenericUser


class CompanyDivisionSerializer(serializers.ModelSerializer):
    user_membership = serializers.SerializerMethodField()
    members_count = serializers.ReadOnlyField()
    name = serializers.CharField(max_length=30)

    class Meta:
        model = CompanyDivision
        read_only_fields = ('company',)
        exclude = ('members',)

    def validate(self, attrs):
        company = self.context['request'].user.genericuser.company
        if not self.instance and company.companydivision_set.filter(
                name=attrs.get('name', None)).count():
            raise serializers.ValidationError(
                'A division with this name already exists')
        # Set company since it is read-only
        attrs.update(company=company)
        instance = CompanyDivision(**attrs)
        instance.clean()
        return attrs

    def get_user_membership(self, obj):
        # Optional: Check if a user (kwarg) is a member of division (obj).
        # Set 'show_user_membership' equal to genericuser.pk or 'self'
        # Returns membership.pk if exists, otherwise None
        member_id_str = self.context.get('request')._request.GET.get(
            'show_user_membership', None)
        if member_id_str:
            try:
                if member_id_str == 'self':
                    member_id = self.context.get('request').user.genericuser.pk
                else:
                    member_id = int(member_id_str)
                user = GenericUser.objects.get(pk=member_id)
                return user.companydivisionmembership_set.get(
                    division=obj.pk).pk
            except Exception:
                return False


class CompanyDivisionMembershipSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyDivisionMembership

    def validate(self, attrs):
        instance = CompanyDivisionMembership(**attrs)
        instance.clean()
        return attrs
