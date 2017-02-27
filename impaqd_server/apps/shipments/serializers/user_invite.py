from rest_framework import serializers
from .generics import UserTypeSerializer
from ..models.user_invite import UserInvite


class UserInviteSerializer(serializers.ModelSerializer):
    user_type = UserTypeSerializer(required=True)
    name = serializers.ReadOnlyField()

    class Meta:
        model = UserInvite
        read_only_fields = ('company',)

    def validate(self, attrs):
        # Set company since it is read-only
        attrs.update(company=self.context['request'].user.genericuser.company)
        instance = UserInvite(**attrs)
        instance.clean()
        return attrs


class UserInviteAcceptSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField()

    class Meta:
        model = UserInvite
        exclude = (
            'created_at', 'updated_at', 'user_type', 'user', 'company', 'id')
        read_only_fields = ('token', 'email', 'first_name', 'last_name',)
