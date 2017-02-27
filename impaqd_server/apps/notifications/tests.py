from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from datetime import timedelta

from ..shipments.factories.generic_user_factory import GenericUserFactory
from ..shipments.factories.shipment_assignment_factory import (
    ShipmentAssignmentFactory)
from ..shipments.factories.user_invite_factory import (
    UserInviteFactory)
from .models.notifications import Notification
from .models.shipment_assignment import ShipmentAssignmentNotif
from .models.user_invite import UserInviteNotif
from .models.signup_internal import SignupInternalNotif
from .models.retention import Day1, Day7, Day15, Day28, Day31, Day38
from .tasks import send_retention_notifs


def validate_notification(notif):
    valid = True
    # Check if there are remaining mergevars
    if '{{' in notif.email_content_html:
        valid = False

    # Check if content wasn't inserted
    if '*|email_content|*' in notif.email_content_html:
        valid = False

    # Check if size of content is greater than the template alone
    if len(notif.email_content_html) < 6640:
        valid = False

    return valid


class NotificationTests(TestCase):
    @classmethod
    def setUpClass(cls):
        # call super, then add your code
        super(cls, NotificationTests).setUpClass()

    @classmethod
    def tearDownClass(cls):
        # add your code first, then call super
        super(cls, NotificationTests).tearDownClass()

    def setUp(self):
        self.sender = GenericUserFactory()
        self.sender_name = self.sender.name
        self.receiver = GenericUserFactory()
        self.receiver_name = self.receiver.name
        self.receiver_email = self.receiver.email
        self.receivers = [GenericUserFactory()]

    def tearDown(self):
        pass

    def test_shipment_assignment_notif(self):
        sa = ShipmentAssignmentFactory(
            parent=self.sender.company, assignee=self.receiver.company)
        n = ShipmentAssignmentNotif.objects.create(
            shipment_assignment=sa, sender=self.sender)
        n.receivers = self.receivers
        n.save()
        ct = ContentType.objects.get_for_model(ShipmentAssignmentNotif)
        self.assertTrue(
            Notification.objects.filter(
                email_sent=True,
                parent_object_id=n.pk,
                parent_content_type=ct).count() > 0)

    def test_user_invite_notif(self):
        invite = UserInviteFactory()
        n = UserInviteNotif.objects.create(
            invite=invite, sender=self.sender,
            receiver_email=self.receiver_email,
            receiver_name=self.receiver_name)
        n.receivers = self.receivers
        n.save()
        ct = ContentType.objects.get_for_model(UserInviteNotif)
        self.assertTrue(
            Notification.objects.filter(
                email_sent=True,
                parent_object_id=n.pk,
                parent_content_type=ct).count() > 0)

    def test_signup_internal_notif(self):
        user = GenericUserFactory()
        n = SignupInternalNotif.objects.create(company=user.company)
        ct = ContentType.objects.get_for_model(SignupInternalNotif)
        self.assertTrue(
            Notification.objects.filter(
                email_sent=True,
                parent_object_id=n.pk,
                parent_content_type=ct).count() > 0)

    def test_retention_day7(self):
        days = 7
        created_at = timezone.now() - timedelta(days=days+1)
        user = GenericUserFactory()
        user.company.created_at = created_at
        user.company.save()
        send_retention_notifs(days, Day7, False)
        notif = Notification.objects.get(
            receiver_email=user.email,
            parent_content_type=ContentType.objects.get_for_model(Day7))
        self.assertTrue(validate_notification(notif))

    def test_retention_day15(self):
        days = 15
        created_at = timezone.now() - timedelta(days=days+1)
        user = GenericUserFactory()
        user.company.created_at = created_at
        user.company.save()
        send_retention_notifs(days, Day15, False)
        notif = Notification.objects.get(
            receiver_email=user.email,
            parent_content_type=ContentType.objects.get_for_model(Day15))
        self.assertTrue(validate_notification(notif))

    def test_retention_day28(self):
        days = 28
        created_at = timezone.now() - timedelta(days=days+1)
        user = GenericUserFactory()
        user.company.created_at = created_at
        user.company.save()
        user.company.subscription.payment_ready = False
        user.company.subscription.save()
        send_retention_notifs(days, Day28, True)
        notif = Notification.objects.get(
            receiver_email=user.email,
            parent_content_type=ContentType.objects.get_for_model(Day28))
        self.assertTrue(validate_notification(notif))

    def test_retention_day31(self):
        days = 31
        created_at = timezone.now() - timedelta(days=days+1)
        user = GenericUserFactory()
        user.company.created_at = created_at
        user.company.save()
        user.company.subscription.payment_ready = False
        user.company.subscription.save()
        send_retention_notifs(days, Day31, True)
        notif = Notification.objects.get(
            receiver_email=user.email,
            parent_content_type=ContentType.objects.get_for_model(Day31))
        self.assertTrue(validate_notification(notif))

    def test_retention_day38(self):
        days = 38
        created_at = timezone.now() - timedelta(days=days+1)
        user = GenericUserFactory()
        user.company.created_at = created_at
        user.company.save()
        user.company.subscription.payment_ready = False
        user.company.subscription.save()
        send_retention_notifs(days, Day38, True)
        notif = Notification.objects.get(
            receiver_email=user.email,
            parent_content_type=ContentType.objects.get_for_model(Day38))
        self.assertTrue(validate_notification(notif))

    def test_retention_not_sending_too_early(self):
        # Test on Day7
        days = 5
        created_at = timezone.now() - timedelta(days=days)
        user = GenericUserFactory()
        user.company.created_at = created_at
        user.company.save()
        send_retention_notifs(7, Day7, False)
        self.assertTrue(
            Notification.objects.filter(
                receiver_email=user.email,
                parent_content_type=ContentType.objects.get_for_model(Day7))
            .count() == 0)

    def test_retention_not_sending_too_late(self):
        # Test on Day7
        days = 9
        created_at = timezone.now() - timedelta(days=days)
        user = GenericUserFactory()
        user.company.created_at = created_at
        user.company.save()
        send_retention_notifs(7, Day7, False)
        self.assertTrue(
            Notification.objects.filter(
                receiver_email=user.email,
                parent_content_type=ContentType.objects.get_for_model(Day7))
            .count() == 0)

    # def test_retention_notif(self):
    #     notif_set = (Day1, Day7, Day15, Day28, Day31, Day38)
    #     for notif in notif_set:
    #         user = GenericUserFactory()
    #         n = notif.objects.create(receiver=user)
    #         ct = ContentType.objects.get_for_model(notif)
    #         self.assertTrue(
    #             Notification.objects.filter(
    #                 email_sent=True,
    #                 parent_object_id=n.pk,
    #                 parent_content_type=ct).count() > 0)
