from rest_framework import serializers
from .generics import CompanyTypeSerializer
from ..models import (
    GenericCompany, CompanyInvite, CompanyRelation, GenericUser)


class RelatedGenericCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = GenericCompany
        fields = ('id', 'company_name', 'dot', 'company_type',)


class CompanyInviteSerializer(serializers.ModelSerializer):
    invitee_company_type = CompanyTypeSerializer()

    class Meta:
        model = CompanyInvite
        fields = (
            'invitee_name', 'invitee_email', 'invitee_dot', 'invitee_phone',
            'invitee_company_type', 'id')

    def validate(self, data):
        inviter_company = self.context.get('request').user.genericuser.company
        # Validate inviter_company and invitee_email unique_together
        invitee_email = data.get('invitee_email', None)
        if invitee_email:
            try:
                CompanyInvite.objects.get(
                    inviter_company=inviter_company,
                    invitee_email=invitee_email)
            except CompanyInvite.DoesNotExist:
                pass
            else:
                raise serializers.ValidationError(
                    'An invite was already sent to that email')
        # Validate inviter_company and invitee_dot unique_together
        invitee_dot = data.get('invitee_dot', None)
        if invitee_dot:
            try:
                CompanyInvite.objects.get(
                    inviter_company=inviter_company,
                    invitee_dot=invitee_dot)
            except CompanyInvite.DoesNotExist:
                pass
            else:
                raise serializers.ValidationError(
                    'An invite was already sent to a company with that DOT '
                    'number')
        # Validate user isn't inviting his/her own company
        if invitee_dot and inviter_company.dot == invitee_dot:
            raise serializers.ValidationError(
                'You cannot invite your own company')
        if invitee_email:
            try:
                if (GenericUser.objects.get(email=invitee_email).company ==
                        inviter_company):
                    raise serializers.ValidationError(
                        'You cannot invite your own company')
            except Exception:
                pass
        # Validate company relations doesn't exist (based on dot and email)
        # First check if company exists
        company = None
        if invitee_dot:
            try:
                company = GenericCompany.objects.filter(dot=invitee_dot)[0]
            except IndexError:
                pass
        if not company and invitee_email:
            try:
                company = GenericUser.objects.filter(
                    email=invitee_email)[0].company
            except IndexError:
                pass
        # Then check if company relations exist
        if company:
            try:
                # Test that relations exist in both directions
                CompanyRelation.objects.get(
                    relation_from=inviter_company,
                    relation_to=company)
                CompanyRelation.objects.get(
                    relation_to=inviter_company,
                    relation_from=company)
            except CompanyRelation.DoesNotExist:
                pass
            else:
                raise serializers.ValidationError(
                    'You have previously been connected to that company')
        return data
