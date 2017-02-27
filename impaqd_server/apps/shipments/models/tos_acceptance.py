import datetime
from django.contrib.gis.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class TOSAcceptanceStatus(object):
    UNSET = 0
    ACCEPTED = 1
    DECLINED = 2

    CHOICES = (
        (UNSET, 'Unset'),
        (ACCEPTED, 'Accepted'),
        (DECLINED, 'Declined'),
    )

    @classmethod
    def valid(cls, status):
        return cls.UNSET <= status <= cls.DECLINED

    ALL_STATUSES = [UNSET, ACCEPTED, DECLINED]


class TOSAcceptance(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    tos_updated_at = models.DateTimeField(auto_now_add=True)
    tos_status = models.IntegerField(
        choices=TOSAcceptanceStatus.CHOICES,
        default=TOSAcceptanceStatus.UNSET)
    tos_version = models.IntegerField(default=1)

    def __unicode__(self):
        # Return user email for admin display purposes
        if hasattr(self, 'genericuser'):
            return self.genericuser.email
        else:
            return ''


@receiver(pre_save, sender=TOSAcceptance)
def tos_acceptance_pre_save(sender, instance, raw, **kwargs):
    instance.tos_updated_at = datetime.datetime.now()
