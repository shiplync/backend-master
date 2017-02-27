from django.db.models.signals import (
    post_delete)
from django.dispatch import receiver
from django.db import models
from django_extensions.db.fields import UUIDField
from ..utils import delete_remote_file


class FileContext(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uuid_value = UUIDField(version=4, auto=True)
    path = models.CharField(max_length=256)
    url_ttl = models.IntegerField(default=30)

    @property
    def file_url(self):
        from impaqd_server.apps.shipments import utils
        return utils.get_expiring_file_url(self)

    def __unicode__(self):
        if hasattr(self, 'genericuser'):
            return "{user: %s}" % self.genericuser.email
        else:
            return "{uuid: %s}" % self.uuid_value


@receiver(post_delete, sender=FileContext)
def file_context_post_delete(sender, instance, **kwargs):
    delete_remote_file(instance)
