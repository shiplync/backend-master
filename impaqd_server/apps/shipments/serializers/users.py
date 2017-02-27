from rest_framework import serializers
from ..models import (
    FileContext, TOSAcceptance, Platform)
from django.contrib.auth.models import User

def check_for_duplicate_user_on_patch(self, data):
    """Checks if another user with that email already exists when patching a
    user email. Throws 400 if another user exists. Should be called on
    is_valid on all user-type serializers
    """
    if self.context.get('request').method == 'PATCH' and data.get('email'):
        users = User.objects.filter(email=data.get('email'))
        if users.count() > 0 and not users[0].email == self.context.get('request').user.email:
            raise serializers.ValidationError('a user with that email already exists')

class FileContextSerializer(serializers.ModelSerializer):
    file_url = serializers.CharField(read_only=True)
    class Meta:
        model = FileContext

class TOSAcceptanceSerializer(serializers.ModelSerializer):
    # TODO: Get rid of shipper_user once we use GenericUser for shippers
    class Meta:
        model = TOSAcceptance
        fields = ('tos_status',)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'id',)                                

class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        exclude = ('user',)
