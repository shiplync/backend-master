from django.http import JsonResponse
from rest_framework import generics, status, viewsets, filters, mixins
from rest_framework.authentication import (
    BasicAuthentication, TokenAuthentication)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from ..shipments.models import GenericUser
from .models import Geolocation, CachedCoordinate, CachedDistance
from ..shipments.permissions import AccessBlockChecker
from .serializers import (
    GeolocationSerializer, CachedCoordinateSerializer,
    CachedDistanceSerializer)

import pprint
pp = pprint.PrettyPrinter(indent=4)

# Create your views here.


class GeolocationsCreateView(generics.CreateAPIView):
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = Geolocation.objects.all()
    serializer_class = GeolocationSerializer

    def post(self, request, *args, **kwargs):
        if hasattr(request.data, '_mutable') and not request.data._mutable:
            return JsonResponse(None, status=status.HTTP_403_FORBIDDEN, safe=False)
        
        try:
            carrierDriver = GenericUser.objects.get(user_id=self.request.user.pk)
            carrierCompany = carrierDriver.company
            request.data['driver'] = carrierDriver.pk
            request.data['carrier'] = carrierCompany.pk
        except GenericUser.DoesNotExist:
            return JsonResponse(None, status=status.HTTP_404_NOT_FOUND, safe=False)

        return super(GeolocationsCreateView, self).post(request, *args, **kwargs)


class FirstResultsSetPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'paginate_by'
    max_page_size = 1


class CachedCoordinateViewSet(
        generics.ListAPIView, mixins.ListModelMixin,
        generics.CreateAPIView, viewsets.GenericViewSet,
        generics.RetrieveAPIView):
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = IsAuthenticated, AccessBlockChecker
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('address', 'address_2', 'city', 'state', 'zip_code',)
    serializer_class = CachedCoordinateSerializer
    queryset = CachedCoordinate.objects.all()
    pagination_class = FirstResultsSetPagination


class CachedDistanceViewSet(
        generics.ListAPIView, mixins.ListModelMixin,
        generics.CreateAPIView, viewsets.GenericViewSet,
        generics.RetrieveAPIView):
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = IsAuthenticated, AccessBlockChecker
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('start_lat', 'end_lat', 'start_lon', 'end_lon',)
    serializer_class = CachedDistanceSerializer
    queryset = CachedDistance.objects.all()
    pagination_class = FirstResultsSetPagination
