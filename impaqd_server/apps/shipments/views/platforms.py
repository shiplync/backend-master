from ..models import Platform
from ..serializers import PlatformSerializer

import django_filters
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authentication import (
    TokenAuthentication, BasicAuthentication)
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, generics, mixins, filters

from distutils.version import LooseVersion


@api_view(['GET'])
# Apple
def check_apple_version(request, version):
    """
    Check if user has the most up to date version.
    SET MIN_VERSION VERSION ACCORDINGLY!
    """
    MIN_VERSION = '2.4.0'
    if request.method == 'GET':
        res = LooseVersion(MIN_VERSION) <= LooseVersion(version)
    return Response({'version_ok': res})


@api_view(['GET'])
# Android
def check_android_version(request, version):
    """
    Check if user has the most up to date version.
    SET MIN_VERSION VERSION ACCORDINGLY!
    """
    MIN_VERSION = '30'
    if request.method == 'GET':
        res = LooseVersion(MIN_VERSION) <= LooseVersion(version)
    return Response({'version_ok': res})


class CompanyDivisionFilter(django_filters.FilterSet):

    class Meta:
        model = Platform
        fields = ['id', 'identifier']


class PlatformView(
        generics.ListAPIView, mixins.ListModelMixin, generics.CreateAPIView,
        viewsets.GenericViewSet, mixins.UpdateModelMixin,
        generics.RetrieveAPIView, generics.DestroyAPIView):

    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.OrderingFilter, filters.DjangoFilterBackend,)
    filter_class = CompanyDivisionFilter

    def get_queryset(self):
        return Platform.objects.filter(user=self.request.user.genericuser)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.genericuser)

    def create(self, request, *args, **kwargs):
        qs = Platform.objects.filter(
            identifier=self.request.data['identifier'],
            platform_type=self.request.data['platform_type'],
            user=self.request.user.genericuser)
        if qs.count() > 0:
            serializer = PlatformSerializer(qs[0])
            return Response(serializer.data)
        else:
            return super(PlatformView, self).create(request, *args, **kwargs)
