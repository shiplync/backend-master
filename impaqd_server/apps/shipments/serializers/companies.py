from rest_framework import serializers, exceptions
from rest_framework.fields import IntegerField
from impaqd_server.apps.shipments.models import GenericCompany


class CarrierCompanySerializer(serializers.ModelSerializer):
    # Validation must be custom handled, because writable nested serializers
    # can't handle unique fields as of DRF 3.2.4
    # See: https://github.com/tomchristie/django-rest-framework/issues/2403
    dot = IntegerField(min_value=1000, max_value=99999999, validators=[],)

    class Meta:
        model = GenericCompany
        exclude = ('owner',)

    def validate_dot(self, value):
        dot = None
        try:
            dot = self.context['request'].user.genericuser.company.dot
        except:
            pass
        try:
            # Check if another company with that dot already exists
            # Exclude own company first, if coming from a PATCH/PUT
            GenericCompany.objects.exclude(dot=dot).get(dot=value)
            raise exceptions.ValidationError('dot already exists')
        except GenericCompany.DoesNotExist:
            pass
        return value


class CarrierCompanySerializerNested(CarrierCompanySerializer):
    pass


class ShipperCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = GenericCompany
        exclude = ('owner',)


class ShipperCompanySerializerNested(ShipperCompanySerializer):
    pass
