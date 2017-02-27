import os
from django.conf import settings
from django.db import models
from django.db.models.signals import (
    post_save)
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Notification(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Add dependency such that instance will be deleted in the event that any
    # required relationships on parent are deleted.
    parent_content_type = models.ForeignKey(ContentType)
    parent_object_id = models.PositiveIntegerField()
    parent = GenericForeignKey('parent_content_type', 'parent_object_id')

    # Sender email should never be changed
    sender_email = models.EmailField(blank=True, null=True)

    # Optionally tie this notification to a user (outbox)
    sender = models.ForeignKey(
        'shipments.GenericUser', blank=True, null=True,
        related_name='notifications_sent')
    sender_name = models.CharField(max_length=200, blank=True, null=True)

    # Optionally tie this notification to a user (inbox)
    receiver = models.ForeignKey(
        'shipments.GenericUser', blank=True, null=True,
        related_name='notifications_received')
    receiver_name = models.CharField(max_length=200, blank=True, null=True)

    # Required for email
    receiver_email = models.EmailField(blank=True, null=True)
    email_subject = models.CharField(max_length=256, blank=True, null=True)
    use_html_template = models.BooleanField(default=True)

    # Optional for email
    email_content_raw = models.TextField(blank=True, null=True)
    email_content_html = models.TextField(blank=True, null=True)
    email_content_html_file = models.TextField(blank=True, null=True)
    email_mergevars = models.TextField(blank=True, null=True)

    # Sent receipts
    email_sent = models.BooleanField(default=False)


@receiver(post_save, sender=Notification)
def notification_send_email(sender, instance, created, raw, **kwargs):
    if not created:
        return
    email_content_raw = ''
    email_content_html = ''
    if instance.email_content_raw:
        try:
            buf = instance.email_content_raw.split('<sec>')
            for p in buf:
                email_content_raw += p
        except Exception, e:
            print "Unable to parse email content (text)"
            print str(e)
            return

    email_content_html = '*|email_content|*' # If no template should be used
    section_wrap = '%s <br>'
    if instance.use_html_template: # Otherwise set template data
        try:
            file_path = os.path.join(
                settings.BASE_DIR,
                'apps/notifications/templates/core/email_template.html')
            with open(file_path, 'rU') as f:
                email_content_html = f.read().replace('\n', '')
        except Exception, e:
            print "Unable to parse email template data"
            print str(e)
            return
        section_wrap = '''<tr style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif; box-sizing: border-box; font-size: 14px; margin: 0; padding: 0;"><td class="content-block" style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 20px;" valign="top">%s</td></tr>'''

    content = ''
    if instance.email_content_html_file:
        # Get content from file
        try:
            file_path = os.path.join(
                settings.BASE_DIR,
                'apps/notifications/templates/' +
                instance.email_content_html_file)
            with open(file_path, 'rU') as f:
                content = f.read().replace('\n', '')
        except Exception, e:
            print "Unable to parse email template data"
            print str(e)
            return
    else:
        # Get content from email_content_html field
        content = instance.email_content_html.replace('\n', '')
    if instance.email_mergevars:
        # Replace vars with values
        for entry in instance.email_mergevars:
            content = content.replace('{{%s}}' % entry[0], str(entry[1]))
    buf = content.split('<sec>')
    html_string = ''
    for p in buf:
        html_string += section_wrap % p
    email_content_html = email_content_html.replace(
        '*|email_content|*', html_string)
    instance.email_content_html = email_content_html
    instance.save()
    try:
        msg = EmailMultiAlternatives(
            body=email_content_raw,
            subject=instance.email_subject,
            from_email='%s <%s>' % (
                instance.sender_name, instance.sender_email),
            headers={'Reply-To': instance.sender_email},
            to=[instance.receiver_email])
        msg.attach_alternative(email_content_html, "text/html")
        msg.send()
        instance.email_sent = True
        instance.save()
    except Exception, e:
        print "Unable to send email"
        print str(e)
        return


class AbstractNotification(models.Model):
    pass

    class Meta:
        abstract = True

    @property
    def is_group_notification(self):
        if hasattr(self, 'receivers') and hasattr(self.receivers, 'all'):
            return True
        else:
            return False


def create_notification_dict(instance):
    # Default fields
    args = {}
    args['sender_email'] = settings.NOTIFICATION_EMAIL
    args['sender_name'] = 'Traansmission'  # Can be overwritten
    args['parent'] = instance
    if hasattr(instance, 'receiver'):
        args['receiver_email'] = instance.receiver.email

    # Set content from instance
    fields = [
        'email_subject', 'email_content_html', 'sender', 'sender_name',
        'receiver', 'receiver_email', 'receiver_name', 'email_content_raw',
        'email_content_html_file', 'email_mergevars']

    for field in fields:
        if hasattr(instance, field):
            args[field] = getattr(instance, field)

    return args


def create_internal_notification_dict(instance):
    # Default fields
    args = {}
    args['sender_email'] = settings.NOTIFICATION_EMAIL
    args['sender_name'] = 'Traansmission'
    args['parent'] = instance
    args['receiver_email'] = settings.NOTIFICATION_EMAIL
    args['receiver_name'] = 'Traansmission team'

    # Set content from instance
    fields = [
        'email_subject', 'email_content_html', 'use_html_template']

    for field in fields:
        if hasattr(instance, field):
            args[field] = getattr(instance, field)
    domain_str = 'Domain: %s\n' % settings.PORTAL_URL
    args['email_content_html'] = domain_str + args['email_content_html']

    return args


@receiver(post_save)
def abstractnotification_create_notification(
        sender, instance, created, raw, **kwargs):
    if (AbstractNotification in sender.__bases__ and
            created and
            not instance.is_group_notification and
            not getattr(instance, 'is_internal_notification', False)):
        args = create_notification_dict(instance)
        Notification.objects.create(**args)


@receiver(post_save)
def abstractnotification_create_internal_notification(
        sender, instance, created, raw, **kwargs):
    if (AbstractNotification in sender.__bases__ and
            created and
            not instance.is_group_notification and
            getattr(instance, 'is_internal_notification', False)):
        args = create_internal_notification_dict(instance)
        Notification.objects.create(**args)


@receiver(post_save)
def abstractnotification_create_group_notification(
        sender, instance, created, raw, **kwargs):
    if (AbstractNotification in sender.__bases__ and
            instance.is_group_notification and
            instance.receivers.all() > 0 and
            not getattr(instance, 'is_internal_notification', False)):
        # Since this will be called after created = True, we need to check
        # that no notifications was previously created.
        ct = ContentType.objects.get_for_model(sender)
        count = Notification.objects.filter(
            parent_object_id=instance.pk,
            parent_content_type=ct).count()
        if count == 0:
            args = create_notification_dict(instance)
            for r in instance.receivers.all():
                args.update(
                    receiver=r, receiver_email=r.email,
                    receiver_name=r.name)
                Notification.objects.create(**args)
