from ..models.equipment_tag import EquipmentTag
from ..models.generic_user import GenericUser
from ..models.shipments import Shipment
from ..serializers.equipment_tag import EquipmentTagSerializer
from impaqd_server.apps.shipments.permissions import AccessBlockChecker
from rest_framework import viewsets, generics, mixins
from rest_framework.authentication import (
    TokenAuthentication, BasicAuthentication)
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import DjangoFilterBackend
from django.contrib.contenttypes.models import ContentType
from .common import ViewValidationError


class EquipmentTagViewSet(
        generics.ListAPIView, mixins.ListModelMixin, generics.CreateAPIView,
        viewsets.GenericViewSet, generics.DestroyAPIView):
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, AccessBlockChecker)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = (
        'assignee_id', 'tag_type', 'tag_category')
    serializer_class = EquipmentTagSerializer
    model = EquipmentTag
    queryset = EquipmentTag.objects.all()

    def check_assignee_permissions(self, assignee):
        # Check that user is allowed to change assignee
        if type(assignee == Shipment):
            if not self.request.user.has_perm('change_shipment', assignee):
                raise ViewValidationError(
                    detail="You do not have permission to modify this "
                    "shipment")
        elif type(assignee == GenericUser):
            if (not assignee.company.pk ==
                    self.request.user.genericuser.company.pk):
                raise ViewValidationError(
                    detail="You cannot change users from other companies")
        else:
            raise ViewValidationError(
                detail="Not a valid assignee type")

    def get_queryset(self):
        # When patch/get/delete a tag, make sure that a valid assignee
        # is supplied and user has permission to modify assignee
        obj_pk = self.request.parser_context.get('kwargs').get('pk', None)
        if obj_pk:
            assignee = None
            try:
                obj = EquipmentTag.objects.get(pk=obj_pk)
                assignee = obj.assignee
            except Exception:
                raise ViewValidationError(
                    detail="Unable to retrieve assignee")
            self.check_assignee_permissions(assignee)
        return EquipmentTag.objects.all()

    def perform_create(self, serializer):
        # When posting a tag, make sure that a valid assignee
        # is supplied and user has permission to modify assignee
        assignee = None
        try:
            ct_string = self.request.data.get('assignee_content_type', '')
            pk = self.request.data.get('assignee_id', None)
            ct = ContentType.objects.get(model=ct_string)
            assignee = ct.model_class().objects.get(pk=pk)
        except Exception:
            raise ViewValidationError(
                detail="Unable to retrieve assignee")
        self.check_assignee_permissions(assignee)
        serializer.save(
            assigner=self.request.user.genericuser)
