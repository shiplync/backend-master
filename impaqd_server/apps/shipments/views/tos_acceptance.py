from ..models.tos_acceptance import TOSAcceptance, TOSAcceptanceStatus
from ..utils import json_response
from ..serializers.users import TOSAcceptanceSerializer

from rest_framework import generics
from rest_framework.authentication import (
    TokenAuthentication, BasicAuthentication)
from rest_framework.permissions import IsAuthenticated


class TOSAcceptanceView(
        generics.CreateAPIView, generics.RetrieveAPIView,
        generics.UpdateAPIView):
    """
    Get or update terms of service acceptance
    """
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = TOSAcceptanceSerializer
    queryset = TOSAcceptance.objects.all()

    def get_object(self):
        instance = self.request.user.genericuser.tos_acceptance
        return instance

    def post(self, request, *args, **kwargs):
        tos = request.user.genericuser.tos_acceptance
        tos.tos_status = TOSAcceptanceStatus.ACCEPTED
        tos.save()
        return json_response({
            'detail': (
                'You have just accepted the latest TOS. '
                'NOTE: POST is deprecated. Use PATCH instead to change '
                'acceptance status.')
        }, status=200)
