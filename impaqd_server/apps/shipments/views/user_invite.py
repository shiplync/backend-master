from rest_framework import generics, viewsets, mixins, filters
from rest_framework.authentication import (
    TokenAuthentication, BasicAuthentication)
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

from impaqd_server.apps.shipments.permissions import (
    AccessBlockChecker, ModelPermissions)
from ..utils import json_response, username_from_email
from ..models.user_invite import UserInvite
from ..models.generic_user import GenericUser
from ..serializers.user_invite import (
    UserInviteSerializer, UserInviteAcceptSerializer)
from .common import (
    ViewValidationError, ViewDoesNotExistError, StandardResultsSetPagination)


class UserInviteViewSet(
        generics.ListAPIView, mixins.ListModelMixin, generics.CreateAPIView,
        viewsets.GenericViewSet, generics.RetrieveAPIView,
        generics.DestroyAPIView):
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, AccessBlockChecker, ModelPermissions)
    serializer_class = UserInviteSerializer
    filter_backends = (filters.OrderingFilter, filters.DjangoFilterBackend,)
    model = UserInvite
    queryset = UserInvite.objects.all()
    pagination_class = StandardResultsSetPagination
    ordering_fields = ('first_name', 'user_type',)

    def get_queryset(self):
        return UserInvite.objects.filter(
            user=None, company=self.request.user.genericuser.company)

    def perform_create(self, serializer):
        serializer.save(
            company=self.request.user.genericuser.company,
            assigner_user=self.request.user.genericuser)


class UserInviteAcceptViewSet(
        viewsets.GenericViewSet, generics.RetrieveAPIView,
        generics.UpdateAPIView):
    serializer_class = UserInviteAcceptSerializer
    model = UserInvite
    queryset = UserInvite.objects.all()

    def get_object(self):
        invite_token = self.kwargs.get('pk', '')
        try:
            # Only choose active invites
            invite = UserInvite.objects.get(token=invite_token)
            if not invite.active:
                raise ViewValidationError(detail='Invite no longer active')
        except UserInvite.DoesNotExist:
            raise ViewDoesNotExistError(detail='Invite does not exist')
        except ValueError:
            raise ViewValidationError(detail='Not a valid token')
        return invite

    def update(self, request, *args, **kwargs):
        password = self.request.data.get('password', '')
        if len(password) == 0:
            raise ViewValidationError(detail='No password supplied')
        instance = self.get_object()
        user = None
        try:
            user = User.objects.create_user(
                username_from_email(instance.email), None, password=password)
            genericuser = GenericUser.objects.create(
                email=instance.email, company=instance.company,
                first_name=instance.first_name, last_name=instance.last_name,
                user_type=instance.user_type, user=user)
            instance.user = genericuser
            instance.save()
        except Exception:
            if user:
                user.delete()
            raise ViewValidationError(
                detail='Unable to create user')
        return json_response({
            'token': str(user.auth_token)
        })
