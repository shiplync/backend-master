from rest_framework import generics
from rest_framework.authentication import (
    TokenAuthentication, BasicAuthentication)
from rest_framework.permissions import IsAuthenticated

from serializers import SubscriptionSerializer
from impaqd_server.apps.shipments.permissions import AccessBlockChecker


class SubscriptionSelfView(generics.RetrieveUpdateAPIView):
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, AccessBlockChecker)
    serializer_class = SubscriptionSerializer

    def get_object(self):
        return self.request.user.genericuser.company.subscription
