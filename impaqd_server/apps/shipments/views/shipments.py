from ..models.shipments import Shipment
from ..models.delivery_status import DeliveryStatus
from ..serializers.shipments import (
    ShipmentSerializer, AddressDetailsSerializer,
    AddressDetailsSerializerClean)

from impaqd_server.apps.shipments.utils import json_response
from common import nested_or_flat_serializer
import django_filters

from rest_framework import viewsets, filters, generics, mixins, renderers
from rest_framework.filters import DjangoObjectPermissionsFilter

from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D

from decimal import *
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes, renderer_classes)
from rest_framework.response import Response
from impaqd_server.apps.shipments.pushNotifications import (
    pushShipmentHandshakeApproved, pushShipmentHandshakeDeclined)
from django.views.decorators.csrf import csrf_exempt

from rest_framework.authentication import (
    TokenAuthentication, BasicAuthentication)
from rest_framework.permissions import IsAuthenticated

from impaqd_server.apps.shipments.permissions import (
    AccessBlockChecker, ObjectPermissions, ModelPermissions)
from impaqd_server.apps.shipments import notifications
from ...geolocations.models import CachedDistance, CachedCoordinate

from ..serializers import ShipmentGeolocationSerializer
from .common import StandardResultsSetPagination

import logging
LOG = logging.getLogger('impaqd')


class ShipmentDistanceFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        distance_filter_radius = request.query_params.get('d_radius')
        distance_filter_latlon = request.query_params.get('d_latlon')
        distance_filter_target = request.query_params.get('d_target')
        ordering_type = request.GET.get('ordering', '')

        point = None
        if distance_filter_latlon:
            try:
                latlon = distance_filter_latlon.split(',')
                point = Point(float(latlon[1]), float(latlon[0]), srid=4326)
            except:
                return queryset

        # Ordering
        if (point and ordering_type == 'proximity'
                and distance_filter_target == 'first_location'):
            queryset = queryset.distance(
                point, field_name='first_location__cached_coordinate__coordinate'
                ).order_by('distance')
        elif (point and ordering_type == 'proximity'
                and distance_filter_target == 'last_location'):
            queryset = queryset.distance(
                point, field_name='last_location__cached_coordinate__coordinate'
                ).order_by('distance')

        # Filtering
        if not (distance_filter_radius and distance_filter_target):
            return queryset
        try:
            radius = float(distance_filter_radius)
            if radius > 0 and distance_filter_target == 'first_location':
                queryset = queryset.filter(
                    first_location__cached_coordinate__coordinate__distance_lt=(
                        point, D(m=radius)))
            elif radius > 0 and distance_filter_target == 'last_location':
                queryset = queryset.filter(
                    last_location__cached_coordinate__coordinate__distance_lt=(
                        point, D(m=radius)))
            return queryset
        except Exception:
            return queryset


class ShipmentFilter(django_filters.FilterSet):
    max_trip_distance = django_filters.NumberFilter(
        name="trip_distance_miles", lookup_type='lte')
    delivery_status = django_filters.MultipleChoiceFilter(
        name="delivery_status", choices=DeliveryStatus.CHOICES)
    delivery_status.always_filter = False  # No unnecessary filtering
    distance_filter = ShipmentDistanceFilter()

    class Meta:
        model = Shipment
        fields = ['id', 'max_trip_distance', 'delivery_status']


class ShipmentViewSet(
        generics.ListAPIView, mixins.ListModelMixin, generics.CreateAPIView,
        mixins.UpdateModelMixin, viewsets.GenericViewSet,
        generics.RetrieveAPIView, generics.DestroyAPIView):
    '''
    View that only returns shipments claimed by a given carrier.
    OR if with_status is ['1'] (array with one string element),
    it returns all unrequested shipments.
    '''
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    filter_backends = (
        DjangoObjectPermissionsFilter, filters.OrderingFilter,
        filters.DjangoFilterBackend, ShipmentDistanceFilter,)
    filter_class = ShipmentFilter
    permission_classes = (
        ModelPermissions, ObjectPermissions, IsAuthenticated,
        AccessBlockChecker)
    ordering_fields = (
        'id', 'first_location__time_range__time_range_end')
    queryset = Shipment.objects.all()
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        return ShipmentSerializer

    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user.genericuser.company,
            owner_user=self.request.user.genericuser)


class CarrierShipmentsSingleView(generics.RetrieveUpdateAPIView):
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, AccessBlockChecker)
    queryset = Shipment.objects.all()

    def get_serializer_class(self):
        return nested_or_flat_serializer('ShipmentSerializer', self.request)

    def perform_update(self, serializer):
        obj = serializer.save()
        carrier_set_self = self.request.data.get('carrier_set_self')
        carrier_set_none = self.request.data.get('carrier_set_none')
        if carrier_set_self:
            carrier = self.request.user.genericuser.company
            # Don't allow carrier to claim the shipment if someone already have
            # claimed it.  # if not carrier.has_active_shipment and not
            # obj.carrier:
            if not obj.carrier:
                serializer.save(carrier=carrier)
        elif carrier_set_none:
            carrier = self.request.user.genericuser.company
            if obj.carrier and carrier.id == obj.carrier.id:
                serializer.save(carrier=None)

    def get_object(self):
        carrier = self.request.user.genericuser.company
        shipment_pk = self.kwargs.get('pk')
        shipment = Shipment.objects.get(id=shipment_pk)
        if shipment and shipment.carrier and shipment.carrier.id != carrier.id:
            return None
        else:
            return shipment


@csrf_exempt
@api_view(['POST'])
@authentication_classes((TokenAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated, AccessBlockChecker,))
def shipperApproveCarrier(request):
    # If we want to store all location updates,
    # we can simply create a shipmenttrackingpoint in this function.
    if request.method == 'POST':
        approved = request.data['approve']
        shipment_id = request.data['shipment_id']
        shipment = None
        try:
            shipment = Shipment.objects.get(pk=shipment_id)
        except Exception:
            print 'Shipment does not exist'
            return json_response({
                'error': 'Shipment does not exist'
            }, status=404)
        carrier = shipment.carrier
        shipper = request.user.genericuser.company
        if approved and carrier and not shipment.carrier_is_approved:
            # Set approved field on shipment
            shipment.carrier_is_approved = True
            shipment.save()
            # Send notification to carrier and internally that
            # shipper has approved inquiry
            notifications.carriers.request_approved(shipment, shipper, carrier)
            notifications.internal.request_approved(shipment, shipper, carrier)
            pushShipmentHandshakeApproved(shipment, carrier, shipper)
            return Response(ShipmentSerializer(shipment).data)
        elif not approved and carrier:
            shipment.carrier = None
            shipment.save()
            # Send notification to carrier and internally that shipper has
            # declined inquiry
            notifications.carriers.request_declined(shipment, shipper, carrier)
            notifications.internal.request_declined(shipment, shipper, carrier)
            pushShipmentHandshakeDeclined(shipment, carrier, shipper)
            return Response(ShipmentSerializer(shipment).data)
        else:
            print 'No carrier can be approved/declined on this shipment'
            return json_response({
                'error': 'Unable to approve/decline carrier'
            }, status=500)
        return Response({'status_ok': True})


@api_view(['GET'])
@authentication_classes((TokenAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
@renderer_classes((renderers.JSONRenderer,))
def shipment_geolocations_list_view(request, *args, **kwargs):
    shipment_pk = kwargs.get('pk', -1)
    queryset = Shipment.objects.none()
    try:
        shipment = Shipment.objects.get(pk=shipment_pk)
        queryset = shipment.geolocation_set.get_queryset().order_by(
            'timestamp')
    except Shipment.DoesNotExist:
        pass
    serializer = ShipmentGeolocationSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes((TokenAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
@renderer_classes((renderers.JSONRenderer,))
def shipment_update_cached_coordinates(request, *args, **kwargs):
    shipment_pk = kwargs.get('pk', -1)
    shipment = None
    try:
        shipment = Shipment.objects.get(pk=shipment_pk)
    except Shipment.DoesNotExist:
        return json_response({
            'error': 'Shipment does not exist'
        }, status=404)
    missing_coordinates = []
    for location in shipment.locations.all():
        # For each location, update of flag cachedcoordinate
        ad = location.address_details
        qs = CachedCoordinate.objects.filter(
            address=ad.address, address_2=ad.address_2, city=ad.city,
            state=ad.state, zip_code=ad.zip_code)
        if qs.count() > 0:
            location.cached_coordinate = qs[0]
        else:
            location.cached_coordinate = None
            serializer = AddressDetailsSerializerClean(ad)
            missing_coordinates.append(serializer.data)
        location.save()
    return Response(missing_coordinates)


@api_view(['GET'])
@authentication_classes((TokenAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
@renderer_classes((renderers.JSONRenderer,))
def shipment_update_cached_distances(request, *args, **kwargs):
    shipment_pk = kwargs.get('pk', -1)
    shipment = None
    try:
        shipment = Shipment.objects.get(pk=shipment_pk)
    except Shipment.DoesNotExist:
        return json_response({
            'error': 'Shipment does not exist'
        }, status=404)
    missing_distances = []
    for location in shipment.locations.all():
        # For each location, update of flag cacheddistance
        start_coord = None
        end_coord = None
        try:
            start_coord = location.cached_coordinate
            end_coord = location.next_location.cached_coordinate
        except Exception:
            # Either location or next_location doesn't have a coordinate or
            # location doesn't have a next_location. We can't do anything.
            pass
        if start_coord and end_coord:
            params = {
                'start_lat': Decimal(str(start_coord.latitude)),
                'start_lon': Decimal(str(start_coord.longitude)),
                'end_lat': Decimal(str(end_coord.latitude)),
                'end_lon': Decimal(str(end_coord.longitude))
            }
            qs = CachedDistance.objects.filter(**params)
            if qs.count() > 0:
                location.cached_distance = qs[0]
            else:
                location.cached_distance = None
                missing_distances.append(params)
        location.save()
    return Response(missing_distances)
