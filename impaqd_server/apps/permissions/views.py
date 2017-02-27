from rest_framework import generics
from rest_framework.authentication import (
    TokenAuthentication, BasicAuthentication)

from .models import BasePermissionCollection
from .serializers import BasePermissionCollectionSerializer


class PermissionRetrieveView(generics.RetrieveAPIView):
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    queryset = BasePermissionCollection.objects.all()
    serializer_class = BasePermissionCollectionSerializer

    def get_object(self):
        return self.request.user.genericuser.permissions
