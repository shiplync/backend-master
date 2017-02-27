from __future__ import unicode_literals

from django.contrib.gis.db import models
from django.utils import timezone
from datetime import timedelta


class Subscription(models.Model):
    no_users = models.IntegerField(null=True, blank=True, default=1)
    no_trucks = models.IntegerField(null=True, blank=True, default=10)
    annual_plan = models.BooleanField(default=True)
    payment_ready = models.BooleanField(default=False)
    trial_start = models.DateTimeField(null=True, blank=True)
    trial_length = models.IntegerField(default=0)

    class Meta:
        pass

    @property
    def trial_active(self):
        return self.trial_length > 0 and (
            self.trial_start + timedelta(days=self.trial_length) >
            timezone.now())
