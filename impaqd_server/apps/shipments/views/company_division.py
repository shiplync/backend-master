import django_filters
from rest_framework import viewsets, generics, mixins, filters
from rest_framework.authentication import (
    TokenAuthentication, BasicAuthentication)
from rest_framework.permissions import IsAuthenticated

from impaqd_server.apps.shipments.permissions import (
    AccessBlockChecker, ModelPermissions)
from .common import StandardResultsSetPagination
from .common import ViewValidationError
from ..models.company_division import (
    CompanyDivision, CompanyDivisionMembership)
from ..serializers.company_division import (
    CompanyDivisionSerializer, CompanyDivisionMembershipSerializer)


class CompanyDivisionFilter(django_filters.FilterSet):

    class Meta:
        model = CompanyDivision
        fields = ['id', 'members']


class CompanyDivisionViewSet(
        generics.ListAPIView, mixins.ListModelMixin, generics.CreateAPIView,
        viewsets.GenericViewSet, mixins.UpdateModelMixin,
        generics.RetrieveAPIView, generics.DestroyAPIView):
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, AccessBlockChecker, ModelPermissions)
    queryset = CompanyDivision.objects.all()
    pagination_class = StandardResultsSetPagination
    filter_backends = (filters.OrderingFilter, filters.DjangoFilterBackend,)
    filter_class = CompanyDivisionFilter
    serializer_class = CompanyDivisionSerializer
    ordering_fields = ('name',)

    def get_queryset(self):
        return CompanyDivision.objects.filter(
            company=self.request.user.genericuser.company)

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.genericuser.company)


class CompanyDivisionMembershipViewSet(
        generics.ListAPIView, mixins.ListModelMixin, generics.CreateAPIView,
        viewsets.GenericViewSet, generics.RetrieveAPIView,
        generics.DestroyAPIView):
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (ModelPermissions, IsAuthenticated, AccessBlockChecker)
    queryset = CompanyDivisionMembership.objects.all()
    pagination_class = StandardResultsSetPagination
    filter_backends = (filters.OrderingFilter, filters.DjangoFilterBackend,)
    serializer_class = CompanyDivisionMembershipSerializer
    ordering_fields = ('id')

    def get_queryset(self):
        return CompanyDivisionMembership.objects.filter(
            division__company=self.request.user.genericuser.company)

    def perform_create(self, serializer):
        if (self.request.user.genericuser.company.pk !=
                serializer.validated_data['division'].company.pk):
            raise ViewValidationError(
                detail='You cannot assign users to divisions in different '
                'companies')
        if (self.request.user.genericuser.company.pk !=
                serializer.validated_data['user'].company.pk):
            raise ViewValidationError(
                detail='You cannot assign users from different companies to '
                'divisions')
        serializer.save()
