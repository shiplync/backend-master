from django.db import models
from django.conf import settings

from .notifications import AbstractNotification


class UserInviteNotif(AbstractNotification):
    invite = models.ForeignKey('shipments.UserInvite')

    sender = models.ForeignKey('shipments.GenericUser')
    receiver_email = models.EmailField()
    receiver_name = models.CharField(max_length=200)

    @property
    def sender_name(self):
        return self.sender.name

    @property
    def email_subject(self):
        return 'Your Traansmission account'

    @property
    def email_content_html(self):
        return (
            'Hi %s,<sec>'
            '%s has invited you to Traansmission.<sec>'
            '<a href=%sregister/user?t=%s>Click here</b> to get started' % (
                self.receiver_name, self.sender_name,
                settings.PORTAL_URL, self.invite.token))
