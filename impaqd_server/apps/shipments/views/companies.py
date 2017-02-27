import django_filters
from rest_framework import viewsets, generics, mixins, filters
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.authentication import (
    TokenAuthentication, BasicAuthentication)
from rest_framework.permissions import IsAuthenticated

from .common import StandardResultsSetPagination
from ..permissions import AccessBlockChecker, ModelPermissions
from ..models.generic_company import GenericCompany
from ..serializers.generics import (
    GenericCompanySerializer, GenericCompanyTeamSerializer)
from impaqd_server.apps.shipments.renderers import (
    CamelCaseJSONRenderer,
    CamelCaseToJSONParser)
from rest_framework import renderers


class CompaniesSelfView(RetrieveUpdateAPIView):
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, AccessBlockChecker)
    parser_classes = (CamelCaseToJSONParser,)

    def get_serializer_class(self):
        return GenericCompanySerializer

    def get_object(self):
        return self.request.user.genericuser.company

    def get_renderers(self):
        """
        If camel_case url arg is set to 1, return JSON with camelCase keys
        """
        camel_case = self.request.GET.get('camel_case', 0)
        if camel_case:
            try:
                camel_case = int(self.request.GET.get('camel_case', 0))
            except ValueError:
                print 'Unable to convert camel_case to int'
                camel_case = 0

            if camel_case == 1:
                return (CamelCaseJSONRenderer(),)
            else:
                return (renderers.JSONRenderer(),)
        else:
            return (renderers.JSONRenderer(),)


class CompanyFilter(django_filters.FilterSet):

    class Meta:
        model = GenericCompany
        fields = ['id', 'company_name']


class CompanyTeamViewSet(
        generics.ListAPIView, mixins.ListModelMixin,
        viewsets.GenericViewSet, generics.RetrieveAPIView):
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, AccessBlockChecker, ModelPermissions)
    queryset = GenericCompany.objects.all()
    pagination_class = StandardResultsSetPagination
    filter_backends = (filters.OrderingFilter, filters.DjangoFilterBackend,)
    filter_class = CompanyFilter
    serializer_class = GenericCompanyTeamSerializer
    ordering_fields = ('company_name',)

    def get_queryset(self):
        return self.request.user.genericuser.company.relations.all()
