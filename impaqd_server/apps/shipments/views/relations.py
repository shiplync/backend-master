from .common import StandardResultsSetPagination
from ..serializers.relations import (
    RelatedGenericCompanySerializer, CompanyInviteSerializer)
from ..models.generic_company import GenericCompany
from ..models.relations import CompanyInvite
from impaqd_server.apps.shipments.permissions import (
    AccessBlockChecker, ModelPermissions)
from rest_framework import generics, viewsets, mixins, filters
from rest_framework.authentication import (
    TokenAuthentication, BasicAuthentication)
from rest_framework.permissions import IsAuthenticated


class RelatedCompaniesListView(generics.ListAPIView):
    serializer_class = RelatedGenericCompanySerializer
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, AccessBlockChecker)
    model = GenericCompany

    def get_queryset(self):
        return self.request.user.genericuser.company.relations.all()


class RelatedCompaniesRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = RelatedGenericCompanySerializer
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    model = GenericCompany

    def get_queryset(self):
        return self.request.user.genericuser.company.relations.all()

    def get_object(self):
        company_pk = self.kwargs.get('pk')
        res = self.request.user.genericuser.company.relations.filter(
            pk=company_pk)
        if res.count():
            obj = res[0]
            return obj


class CompanyInviteViewSet(
        generics.ListAPIView, mixins.ListModelMixin,
        generics.CreateAPIView, mixins.UpdateModelMixin,
        viewsets.GenericViewSet, generics.RetrieveAPIView,
        generics.DestroyAPIView):
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (ModelPermissions, IsAuthenticated, AccessBlockChecker)
    serializer_class = CompanyInviteSerializer
    filter_backends = (filters.OrderingFilter, filters.DjangoFilterBackend,)
    model = CompanyInvite
    queryset = CompanyInvite.objects.all()
    pagination_class = StandardResultsSetPagination
    ordering_fields = ('invitee_name', 'invitee_company_type',)

    def perform_create(self, serializer):
        serializer.save(
            inviter_user=self.request.user.genericuser,
            inviter_company=self.request.user.genericuser.company)

    def get_queryset(self):
        return CompanyInvite.objects.filter(
            invite_accepted=False,
            inviter_user=self.request.user.genericuser)
