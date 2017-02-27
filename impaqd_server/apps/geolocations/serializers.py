from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import Geolocation, CachedCoordinate, CachedDistance
from .validators import LatitudeValidator, LongitudeValidator
from ..shipments.models.generic_user import GenericUser
from ..shipments.models.generic_company import GenericCompany


class GeolocationSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(read_only=False)
    longitude = serializers.FloatField(read_only=False)
    altitude = serializers.FloatField(read_only=False)
    accuracy = serializers.FloatField(read_only=False)
    speed = serializers.FloatField(read_only=False)
    course = serializers.FloatField(read_only=False)
    timestamp = serializers.DateTimeField(read_only=False)

    carrier = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=GenericCompany.objects.all())
    driver = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=GenericUser.objects.all())
    
    class Meta:
        model = Geolocation

    def validate_latitude(self, value):
        try:
            LatitudeValidator()(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def validate_longitude(self, value):
        try:
            LongitudeValidator()(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value


class CachedCoordinateSerializer(serializers.ModelSerializer):
    latitude = serializers.DecimalField(
        read_only=True, max_digits=13, decimal_places=10)
    longitude = serializers.DecimalField(
        read_only=True, max_digits=13, decimal_places=10)

    class Meta:
        model = CachedCoordinate
        exclude = ('id', 'created_at', 'updated_at',)


class CachedDistanceSerializer(serializers.ModelSerializer):
    pass

    class Meta:
        model = CachedDistance
        exclude = ('id', 'created_at', 'updated_at',)
