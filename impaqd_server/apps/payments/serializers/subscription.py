from rest_framework import serializers

from ..models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    no_users = serializers.IntegerField()
    no_trucks = serializers.IntegerField()

    class Meta:
        model = Subscription

    def validate(self, attrs):

        no_users = int(self.context['request'].data['no_users'])
        no_trucks = int(self.context['request'].data['no_trucks'])
        if no_users < 1 or no_users > 20:
            raise serializers.ValidationError(
                'Number of users is out of bound.')
        if no_trucks < 0 or no_trucks > 50:
            raise serializers.ValidationError(
                'Number of trucks is out of bound.')

        return attrs
