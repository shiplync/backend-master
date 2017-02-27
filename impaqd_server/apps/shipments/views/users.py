from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponseBadRequest, HttpResponseNotFound, HttpResponse
from django.views.generic import ListView
from rest_framework import renderers
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import django_filters
from rest_framework import viewsets, generics, mixins, filters
from django.contrib.auth import get_user_model
from common import nested_or_flat_serializer, StandardResultsSetPagination
from ..permissions import AccessBlockChecker, ModelPermissions
from ..models.generic_user import GenericUser
from ..serializers.generics import GenericUserTeamSerializer
from impaqd_server.apps.shipments.renderers import (
    CamelCaseJSONRenderer,
    CamelCaseToJSONParser)

# Create your views here.


# TODO: Use rest_framework view instead of native Django view if possible
class UsersListView(ListView):
    model = get_user_model()

    def head(self, request, *args, **kwargs):
        if request.GET.__contains__('email'):
            email = request.GET.get('email', None)
            try:
                self.get_queryset().get(email=email)
                return HttpResponse(status=204)
            except ObjectDoesNotExist:
                return HttpResponseNotFound()
        return HttpResponseBadRequest()


class UsersSelfView(RetrieveUpdateAPIView):
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, AccessBlockChecker)
    parser_classes = (CamelCaseToJSONParser,)

    def get_serializer_class(self):
        return nested_or_flat_serializer('GenericUserSerializer', self.request)

    def get_object(self):
        return self.request.user.genericuser

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


class GenericUserFilter(django_filters.FilterSet):

    class Meta:
        model = GenericUser
        fields = ['id', 'first_name', 'user_type', 'companydivision']


class UserTeamViewSet(
        generics.ListAPIView, mixins.ListModelMixin,
        mixins.UpdateModelMixin, viewsets.GenericViewSet,
        generics.RetrieveAPIView, generics.DestroyAPIView):
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, AccessBlockChecker, ModelPermissions)
    queryset = GenericUser.objects.all()
    pagination_class = StandardResultsSetPagination
    filter_backends = (filters.OrderingFilter, filters.DjangoFilterBackend,)
    filter_class = GenericUserFilter
    serializer_class = GenericUserTeamSerializer
    ordering_fields = ('first_name', 'last_name', 'user_type',)

    def get_queryset(self):
        return_self = self.request.GET.get('return_self', None)
        if return_self:
            return GenericUser.objects.filter(
                company=self.request.user.genericuser.company)
        else:
            return GenericUser.objects.filter(
                company=self.request.user.genericuser.company).exclude(
                    pk=self.request.user.genericuser.pk)
