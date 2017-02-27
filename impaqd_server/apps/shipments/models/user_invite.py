from django.db.models.signals import (
    post_save, post_delete)
from django.dispatch import receiver
from django.contrib.gis.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .generic_user import GenericUser, UserType
from ...notifications.models.user_invite import UserInviteNotif
import uuid


class UserInvite(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    company = models.ForeignKey('GenericCompany')
    assigner_user = models.ForeignKey(
        'GenericUser', null=True, blank=True, related_name='invited_users')
    user_type = models.CharField(
        max_length=200, choices=UserType.CHOICES, default=UserType.UNKNOWN)
    user = models.OneToOneField(
        'GenericUser', default=None, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ('first_name',)

    @property
    def name(self):
        return ((self.first_name + ' ' + self.last_name) if self.first_name
                and self.last_name else self.first_name)

    @property
    def active(self):
        return self.user is None

    def clean(self):
        if (self.email is not None and
                GenericUser.objects.filter(email=self.email).count()):
            raise ValidationError(_('A user with this email already exists'))
        if self.company.remaining_user_invites < 1:
            raise ValidationError(_(
                'This company has exceeded its new user limit'))


@receiver(post_save, sender=UserInvite)
def userinvite_send_invite(sender, instance, created, raw, **kwargs):
    if created:
        invite_sender = (
            instance.assigner_user if instance.assigner_user else
            instance.company.owner)

        UserInviteNotif.objects.create(
            receiver_email=instance.email, receiver_name=instance.name,
            invite=instance, sender=invite_sender)
