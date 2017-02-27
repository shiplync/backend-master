from django.db import models

from .notifications import AbstractNotification


class Day1(AbstractNotification):
    receiver = models.OneToOneField('shipments.GenericUser')

    @property
    def email_subject(self):
        return 'Welcome to Traansmission'

    @property
    def email_content_html_file(self):
        return 'retention_day_1.html'

    @property
    def email_mergevars(self):
        return (('receiver_name', self.receiver.first_name),)


class Day7(AbstractNotification):
    receiver = models.OneToOneField('shipments.GenericUser')

    @property
    def email_subject(self):
        return 'Tips and tricks'

    @property
    def email_content_html_file(self):
        return 'retention_day_7.html'

    @property
    def email_mergevars(self):
        return (('receiver_name', self.receiver.first_name),)


class Day15(AbstractNotification):
    receiver = models.OneToOneField('shipments.GenericUser')

    @property
    def email_subject(self):
        return 'Checking in'

    @property
    def email_content_html_file(self):
        return 'retention_day_15.html'

    @property
    def email_mergevars(self):
        return (('receiver_name', self.receiver.first_name),)


class Day28(AbstractNotification):
    receiver = models.OneToOneField('shipments.GenericUser')

    @property
    def email_subject(self):
        return 'Next steps with Traansmission!'

    @property
    def email_content_html_file(self):
        return 'retention_day_28.html'

    @property
    def email_mergevars(self):
        return (('receiver_name', self.receiver.first_name),)


class Day31(AbstractNotification):
    receiver = models.OneToOneField('shipments.GenericUser')

    @property
    def email_subject(self):
        return 'This doesn\'t have to be the end'

    @property
    def email_content_html_file(self):
        return 'retention_day_31.html'

    @property
    def email_mergevars(self):
        return (('receiver_name', self.receiver.first_name),)


class Day38(AbstractNotification):
    receiver = models.OneToOneField('shipments.GenericUser')

    @property
    def email_subject(self):
        return 'Traansmission misses you'

    @property
    def email_content_html_file(self):
        return 'retention_day_38.html'

    @property
    def email_mergevars(self):
        return (('receiver_name', self.receiver.first_name),)
