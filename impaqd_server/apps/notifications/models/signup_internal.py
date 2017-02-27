from django.db import models
from .notifications import AbstractNotification


class SignupInternalNotif(AbstractNotification):
    company = models.ForeignKey('shipments.GenericCompany')

    @property
    def email_subject(self):
        return 'New user signup'

    @property
    def is_internal_notification(self):
        return True

    @property
    def email_content_html(self):
        content = ''
        content += 'Contact name: %s <br>' % self.company.owner.name
        content += 'Contact email: %s <br>' % self.company.owner.email

        return content
