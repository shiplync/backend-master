from ..serializers.shipment_assignment import (
    ShipmentAssignmentSerializer, ShipmentCarrierAssignmentSerializer,
    ShipmentDriverAssignmentSerializer)
from ..models.shipments import Shipment
from ..models.shipment_assignment import (
    ShipmentAssignment, ShipmentCarrierAssignment, ShipmentDriverAssignment)
from ..models.generic_user import GenericUser
from ..models.generic_company import GenericCompany
from ..models.delivery_status import DeliveryStatus
from ..models.company_division import CompanyDivision
from impaqd_server.apps.shipments.permissions import (
    AccessBlockChecker, ModelPermissions)
from rest_framework import generics, viewsets, mixins
from rest_framework.authentication import (
    TokenAuthentication, BasicAuthentication)
from rest_framework.permissions import IsAuthenticated
from django.contrib.contenttypes.models import ContentType
from rest_framework.exceptions import APIException
from rest_framework.filters import DjangoFilterBackend


class ShipmentAssignmentValidationError(APIException):
    status_code = 400


def validate_shipmentassignment(data):
    assignee_content_type = data.get('assignee_content_type', '')
    if not (assignee_content_type == 'genericuser' or
            assignee_content_type == 'companydivision' or
            assignee_content_type == 'genericcompany'):
            raise ShipmentAssignmentValidationError(
                detail='Invalid assignee_content_type')
    assignee_id = data.get('assignee_id', 0)
    try:
        ct = ContentType.objects.get(model=assignee_content_type)
        assignee_model = ct.model_class()
        assignee_model.objects.get(pk=assignee_id)
    except:
        raise ShipmentAssignmentValidationError(
            'object assignee_id does not exist')
    shipment_id = data.get('shipment', '')
    shipment = None
    try:
        shipment = Shipment.objects.get(pk=shipment_id)
    except Shipment.DoesNotExist:
        raise ShipmentAssignmentValidationError(
            'Shipment does not exist')
    if (shipment and shipment.delivery_status in
            DeliveryStatus.CARRIER_APPROVED_STATUSES):
        raise ShipmentAssignmentValidationError(
            'This cannot be done when shipment already has an approved '
            'carrier')


class ShipmentAssignmentViewSet(
        generics.ListAPIView, mixins.ListModelMixin, generics.CreateAPIView,
        viewsets.GenericViewSet, generics.RetrieveAPIView,
        generics.DestroyAPIView):
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, AccessBlockChecker)
    serializer_class = ShipmentAssignmentSerializer
    filter_backends = (DjangoFilterBackend,)
    model = ShipmentAssignment
    queryset = ShipmentAssignment.objects.all()

    def get_queryset(self):
        queryset = ShipmentAssignment.objects.filter(
            assigner=self.request.user.genericuser)
        shipment = None
        try:
            shipment = int(self.request.GET.get('shipment', ''))
        except:
            pass
        if shipment:
            queryset = queryset.filter(shipment_id=shipment)
        content_type = self.request.GET.get('assignee_content_type', '')
        ct = None
        try:
            ct = ContentType.objects.get(model=content_type)
        except:
            pass
        if ct:
            queryset = queryset.filter(assignee_content_type=ct)

        return queryset

    def destroy(self, request, pk, *args, **kwargs):
        a = None
        try:
            a = ShipmentAssignment.objects.get(pk=pk)
        except ShipmentAssignment.DoesNotExist:
            pass
        if (a.shipment.delivery_status in
                DeliveryStatus.CARRIER_APPROVED_STATUSES):
            raise ShipmentAssignmentValidationError(
                'This cannot be done when shipment already has an approved '
                'carrier')
        return super(
            ShipmentAssignmentViewSet, self).destroy(
                self, request, pk, *args, **kwargs)


class ShipmentCarrierAssignmentViewSet(
        generics.CreateAPIView, viewsets.GenericViewSet,
        generics.RetrieveAPIView, generics.DestroyAPIView):
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, AccessBlockChecker, ModelPermissions)
    serializer_class = ShipmentCarrierAssignmentSerializer
    queryset = ShipmentCarrierAssignment.objects.all()


class ShipmentDriverAssignmentViewSet(
        generics.CreateAPIView, viewsets.GenericViewSet,
        generics.RetrieveAPIView, generics.DestroyAPIView):
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, AccessBlockChecker, ModelPermissions)
    serializer_class = ShipmentDriverAssignmentSerializer
    queryset = ShipmentDriverAssignment.objects.all()
