from django.db import models


class Insurance(models.Model):
    policy_url = models.CharField(max_length=2048, null=True, blank=True)
