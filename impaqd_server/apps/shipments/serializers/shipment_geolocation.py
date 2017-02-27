from rest_framework import serializers
from ...geolocations.models import Geolocation


class ShipmentGeolocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Geolocation
        fields = ('latitude', 'longitude', 'timestamp', 'display_text')
