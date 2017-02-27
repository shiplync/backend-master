from django.utils import timezone
from celery import shared_task
from datetime import timedelta
from django.contrib.contenttypes.models import ContentType

from ..shipments.models.generic_company import GenericCompany
from .models.retention import Day7, Day15, Day28, Day31, Day38


def send_retention_notifs(days, notif, unpaid_only):
    model_name = ContentType.objects.get_for_model(notif).model
    kwargs = {}
    kwargs['owner__%s__isnull' % model_name] = False
    now = timezone.now()
    grace_hours = 48
    companies = GenericCompany.objects.exclude(**kwargs).filter(
        created_at__lt=(now - timedelta(days=days)),
        created_at__gt=(now - timedelta(days=days, hours=grace_hours)))
    if unpaid_only:
        companies = companies.exclude(
            subscription__payment_ready=True)
    for c in companies:
        if not hasattr(c.owner, model_name):
            notif.objects.create(receiver=c.owner)


@shared_task(ignore_result=True)
def task_send_retention_notifications():
    send_retention_notifs(7, Day7, False)
    send_retention_notifs(15, Day15, False)
    send_retention_notifs(28, Day28, True)
    send_retention_notifs(31, Day31, True)
    send_retention_notifs(38, Day38, True)


@shared_task(ignore_result=True)
def task_test():
    print 'test'
