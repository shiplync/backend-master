from rest_framework import serializers
import carriers
from .common import update_object, obj_permissions
from .equipment_tag import EquipmentTagSerializer
from impaqd_server.apps.shipments.models import (
    Shipment, ShipmentLocation, ShipmentRequest, SavedLocation, TimeRange,
    ShipmentPayout, ShipmentFeatures, Person, DeliveryStatus)
from ..models.generic_user import GenericUser
from ..models.generic_company import GenericCompany
from ..models.locations import AddressDetails, LocationType
from django.contrib.gis.geos import Point


class PointField(serializers.Field):
    """
    A field for handling GeoDjango Point fields as a json format.
    Expected input format:
        {
        "latitude": 49.8782482189424,
         "longitude": 24.452545489
        }

    """
    type_name = 'PointField'
    type_label = 'point'

    default_error_messages = {
        'invalid': (
            'Location field has wrong format. '
            'Use {"latitude": 45.67294621, "longitude": 26.43156}'),
        }

    def to_internal_value(self, value):
        """
        Parse json data and return a point object
        """
        # try:
        #     value = json.loads(value)
        # except ValueError:
        #     value = None

        if value:
            latitude = value.get("latitude")
            longitude = value.get("longitude")
            if latitude and longitude:
                return Point(longitude, latitude)
        msg = self.error_messages['invalid']
        raise serializers.ValidationError(msg)

    def to_representation(self, value):
        """
        Transform POINT object to json.
        """
        bundle = {
            "latitude": value.y,
            "longitude": value.x
        }
        return bundle
        # return json.dumps(bundle)


class NationalPhoneField(serializers.Field):
    # country_code should be made more generic at some point to support
    # localization
    country_code = 1

    def to_representation(self, obj):
        if obj and obj.national_number:
            return str(obj.national_number)
        else:
            return obj

    def to_internal_value(self, data):
        try:
            # Append country code to phone number
            result = (
                '+%i%s' % (self.country_code, data)
                if not data[0:1] == '+' else data)
        except:
            result = data
        return result


class PersonSerializer(serializers.ModelSerializer):
    # phone = NationalPhoneField(required=False, allow_null=True)
    phone_country_code = serializers.ReadOnlyField()
    name = serializers.ReadOnlyField()

    class Meta:
        model = Person


class ShipmentPayoutSerializer(serializers.ModelSerializer):
    payout_distance = serializers.ReadOnlyField()
    missing_fields = serializers.JSONField(read_only=True)

    class Meta:
        model = ShipmentPayout


class TimeRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeRange


class ShipmentFeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentFeatures


class ShipmentCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = GenericCompany
        fields = ('id', 'company_name', 'dot',)


class ShipmentUserSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField()

    class Meta:
        model = GenericUser
        fields = ('id', 'first_name', 'last_name', 'name',)


class AddressDetailsSerializer(serializers.ModelSerializer):
    latitude = serializers.DecimalField(
        read_only=True, max_digits=13, decimal_places=10)
    longitude = serializers.DecimalField(
        read_only=True, max_digits=13, decimal_places=10)

    class Meta:
        model = AddressDetails


class AddressDetailsSerializerClean(serializers.ModelSerializer):
    pass

    class Meta:
        model = AddressDetails
        exclude = ('id', 'created_at', 'updated_at',)


class LocationTypeSerializer(serializers.BaseSerializer):
    def to_representation(self, val):
        status = filter(
            lambda x: x[0] == val, LocationType.CHOICES)[0]
        return {
            'value': status[0],
            'label': status[1]
        }

    def to_internal_value(self, data):
        result = data
        if isinstance(data, dict) and 'value' in data:
            result = data['value']
        # Validate it is a valid choice
        if len(filter(lambda x: x[0] == result, LocationType.CHOICES)):
            return result
        else:
            raise serializers.ValidationError('Not a valid location type')


class LocationSerializer(serializers.ModelSerializer):
    address_details = AddressDetailsSerializer(required=False)
    contact = PersonSerializer(required=False)
    features = ShipmentFeaturesSerializer(required=False)
    time_range = TimeRangeSerializer(required=False)
    location_type = LocationTypeSerializer()
    distance_to_next_location = serializers.ReadOnlyField()
    latitude = serializers.ReadOnlyField()
    longitude = serializers.ReadOnlyField()
    shipment = serializers.PrimaryKeyRelatedField(
        queryset=Shipment.objects.all())

    class Meta:
        model = ShipmentLocation
        read_only_fields = (
            'created_at', 'updated_at', 'arrival_time',)
        exclude = ('cached_distance', 'cached_coordinate',)

    def create(self, validated_data):
        address_details = AddressDetails.objects.create(
            **validated_data.pop('address_details', {}))
        contact = Person.objects.create(
            **validated_data.pop('contact', {}))
        features = ShipmentFeatures.objects.create(
            **validated_data.pop('features', {}))
        time_range = TimeRange.objects.create(
            **validated_data.pop('time_range', {}))
        shipment = validated_data.pop('shipment', {})

        return ShipmentLocation.objects.create(
            contact=contact, features=features, time_range=time_range,
            shipment=shipment, address_details=address_details,
            **validated_data)

    def update(self, instance, validated_data):
        update_object(
            validated_data.pop('address_details', {}),
            instance.address_details)
        update_object(
            validated_data.pop('contact', {}), instance.contact)
        update_object(
            validated_data.pop('features', {}), instance.features)
        update_object(
            validated_data.pop('time_range', {}), instance.time_range)
        update_object(validated_data, instance)

        return instance


class SavedLocationSerializer(serializers.ModelSerializer):
    address_details = AddressDetailsSerializer(required=False)
    contact = PersonSerializer(required=False)
    features = ShipmentFeaturesSerializer(required=False)
    time_range = TimeRangeSerializer(required=False)
    location_type = LocationTypeSerializer()
    latitude = serializers.ReadOnlyField()
    longitude = serializers.ReadOnlyField()

    class Meta:
        model = SavedLocation
        read_only_fields = ('created_at', 'updated_at', 'owner')

    def create(self, validated_data):
        address_details = AddressDetails.objects.create(
            **validated_data.pop('address_details', {}))
        contact = Person.objects.create(
            **validated_data.pop('contact', {}))
        features = ShipmentFeatures.objects.create(
            **validated_data.pop('features', {}))
        time_range = TimeRange.objects.create(
            **validated_data.pop('time_range', {}))

        return SavedLocation.objects.create(
            contact=contact, features=features, time_range=time_range,
            address_details=address_details, **validated_data)

    def update(self, instance, validated_data):
        update_object(
            validated_data.pop('address_details', {}),
            instance.address_details)
        update_object(
            validated_data.pop('contact', {}), instance.contact)
        update_object(
            validated_data.pop('features', {}), instance.features)
        update_object(
            validated_data.pop('time_range', {}), instance.time_range)
        update_object(validated_data, instance)

        return instance


class LocationSerializerPartial(LocationSerializer):
    class Meta:
        model = ShipmentLocation
        fields = ('city', 'state',)


class DeliveryStatusSerializer(serializers.BaseSerializer):
    def to_representation(self, val):
        status = filter(
            lambda x: x[0] == val, DeliveryStatus.CHOICES)[0]
        return {
            'value': status[0],
            'label': status[1]
        }


class ShipmentSerializer(serializers.ModelSerializer):
    # We can not serialize this field when its in read_only_fields.
    # Should it be there?
    # shipper_owner = ShipperSerializer(required=False)
    carrier = ShipmentCompanySerializer(read_only=True)
    carrier_driver = ShipmentUserSerializer(read_only=True)
    payout_info = ShipmentPayoutSerializer(required=False)
    locations = LocationSerializer(many=True, read_only=True)
    delivery_status = DeliveryStatusSerializer(read_only=True)
    equipmenttags = EquipmentTagSerializer(many=True, read_only=True)
    assigned_companies_count = serializers.ReadOnlyField()
    pending_requests_count = serializers.ReadOnlyField()
    trip_distance = serializers.ReadOnlyField()
    permissions = serializers.SerializerMethodField()
    owner = ShipmentCompanySerializer(read_only=True)
    owner_user = ShipmentUserSerializer(read_only=True)
    assigned_carrier = ShipmentCompanySerializer(read_only=True)
    assigned_driver = ShipmentUserSerializer(read_only=True)

    class Meta:
        model = Shipment
        read_only_fields = ('first_location', 'last_location',)

    def create(self, validated_data):
        payout_info = ShipmentPayout.objects.create(
            **validated_data.pop('payout_info', {}))
        owner = validated_data.pop('owner')
        owner_user = validated_data.pop('owner_user')

        return Shipment.objects.create(
            payout_info=payout_info,
            owner=owner, owner_user=owner_user, **validated_data)

    def update(self, instance, validated_data):
        update_object(
            validated_data.pop('payout_info', {}), instance.payout_info)
        update_object(validated_data, instance)

        return instance

    def get_permissions(self, obj):
        return obj_permissions(self, obj)


class ShipmentSerializerPartial(ShipmentSerializer):
    pass


class ShipmentRequestSerializer(serializers.ModelSerializer):
    shipment = ShipmentSerializer
    # We can not serialize this field when its in read_only_fields.
    # Should it be there?
    # carrier = CarrierSerializer
    driver = carriers.CarrierDriverSerializer(required=False)

    class Meta:
        model = ShipmentRequest
        read_only_fields = ('carrier',)
