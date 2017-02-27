from django.db import models
from .notifications import AbstractNotification


class ShipmentAssignmentNotif(AbstractNotification):
    shipment_assignment = models.ForeignKey('shipments.ShipmentAssignment')
    sender = models.ForeignKey('shipments.GenericUser')
    receivers = models.ManyToManyField(
        'shipments.GenericUser', related_name='shipmentassignmentnotif_inbox')

    @property
    def sender_name(self):
        return self.sender.name

    @property
    def email_subject(self):
        return 'New Shipment'

    @property
    def email_content_html(self):
        return (
            '%s from %s has shared a shipment with you.\n' % (
                self.sender.name, self.sender.company.company_name))
