from .common import StandardResultsSetPagination
from ..serializers.shipments import ShipmentRequestSerializer
from ..models.shipments import ShipmentRequest
from ..models.generic_user import UserType
from impaqd_server.apps.shipments.permissions import (
    AccessBlockChecker)

from rest_framework import generics, mixins, viewsets, filters
from rest_framework.authentication import (
    TokenAuthentication, BasicAuthentication)
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser


class CarrierRequestView(
        generics.ListAPIView, mixins.ListModelMixin, generics.CreateAPIView,
        mixins.UpdateModelMixin, viewsets.GenericViewSet,
        generics.RetrieveAPIView, generics.DestroyAPIView):
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, AccessBlockChecker)
    serializer_class = ShipmentRequestSerializer
    queryset = ShipmentRequest.objects.all()
    filter_backends = (filters.OrderingFilter,)
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = ShipmentRequest.objects.filter(
            carrier=self.request.user.genericuser.company)
        return queryset

    def perform_create(self, serializer):
        serializer.save(carrier=self.request.user.genericuser.company)
        # if this is a carrierdriver, set driver on request
        if self.request.user.genericuser.user_type == UserType.CARRIER_DRIVER:
            serializer.save(driver=self.request.user.genericuser)


class CarrierSelfRequestView(generics.ListAPIView):
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, AccessBlockChecker)
    queryset = ShipmentRequest.objects.all()
    serializer_class = ShipmentRequestSerializer

    def get_queryset(self):
        queryset = ShipmentRequest.objects.filter(
            driver=self.request.user.genericuser)
        return queryset


class ShipmentRequestView(viewsets.GenericViewSet):
    queryset = ShipmentRequest.objects.all()
    serializer_class = ShipmentRequestSerializer
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)
