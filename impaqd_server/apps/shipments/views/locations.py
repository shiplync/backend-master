from ..models.shipments import Shipment
from ..models.locations import ShipmentLocation, SavedLocation
from ..serializers.shipments import LocationSerializer, SavedLocationSerializer
from .common import ViewValidationError, StandardResultsSetPagination

from impaqd_server.apps.shipments.permissions import (
    AccessBlockChecker, ModelPermissions)

from rest_framework import viewsets, generics, mixins, filters
from rest_framework.authentication import (
    TokenAuthentication, BasicAuthentication)
from rest_framework.permissions import IsAuthenticated
import django_filters

import logging
LOG = logging.getLogger('impaqd')


class LocationBelongToShipperView(
        generics.CreateAPIView, mixins.UpdateModelMixin,
        viewsets.GenericViewSet, generics.RetrieveAPIView,
        generics.DestroyAPIView, mixins.ListModelMixin):
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, AccessBlockChecker,)
    queryset = ShipmentLocation.objects.all()

    def get_queryset(self):
        # When patch/get/delete a location, make sure that a valid location arg
        # is supplied and user has permission to modify shipment
        location_pk = self.request.parser_context.get('kwargs').get('pk')
        if location_pk:
            shipment = ShipmentLocation.objects.get(
                pk=location_pk).shipment
            if not self.request.user.has_perm('view_shipment', shipment):
                raise ViewValidationError(
                    detail="You do not have permission to this location")
            return ShipmentLocation.objects.filter(
                shipment=shipment)
        return None

    def perform_create(self, serializer):
        # When posting a location, make sure that a valid shipment arg
        # is supplied and user has permission to modify shipment
        shipment = None
        try:
            shipment_pk = self.request.data.get('shipment')
            shipment = Shipment.objects.get(pk=shipment_pk)
        except:
            raise ViewValidationError(
                detail="A valid shipment id is a required argument")
        if not self.request.user.has_perm('change_shipment', shipment):
            raise ViewValidationError(
                detail="You do not have permission to modify this shipment")
        serializer.save()

    def get_serializer_class(self):
        return LocationSerializer


class SavedLocationFilter(django_filters.FilterSet):
    pass

    class Meta:
        model = SavedLocation
        fields = ['id']


class SavedLocationViewSet(
        generics.ListAPIView, mixins.ListModelMixin, generics.CreateAPIView,
        mixins.UpdateModelMixin, viewsets.GenericViewSet,
        generics.RetrieveAPIView, generics.DestroyAPIView):
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, AccessBlockChecker, ModelPermissions)
    queryset = SavedLocation.objects.all()
    pagination_class = StandardResultsSetPagination
    filter_backends = (filters.OrderingFilter, filters.DjangoFilterBackend,)
    filter_class = SavedLocationFilter
    ordering_fields = (
        'id', 'company_name', 'address_details__city', 'updated_at',)

    def get_queryset(self):
        return SavedLocation.objects.filter(
            owner=self.request.user.genericuser.company)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.genericuser.company)

    def get_serializer_class(self):
        return SavedLocationSerializer
