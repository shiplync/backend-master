from django.contrib.gis.db import models
from datetime import timedelta
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from impaqd_server.apps.shipments import notifications
from .generic_user import GenericUser
from .generic_company import GenericCompany, CompanyType


class CompanyRelation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    relation_from = models.ForeignKey(
        'GenericCompany', related_name='from_relations')
    relation_to = models.ForeignKey(
        'GenericCompany', related_name='to_relations')
    is_inviter = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    hidden = models.BooleanField(default=False)
    sibling = models.ForeignKey(
        'self', null=True, blank=True, help_text='The corresponding '
        'CompanyRelation with relation_from and relation_to reversed')

    class Meta:
        unique_together = (('relation_from', 'relation_to'),)

    def __unicode__(self):
        return self.relation_from.__unicode__()


@receiver(post_save, sender=CompanyRelation)
def company_relation_post_save(sender, instance, created, raw, **kwargs):
    if created:
        # If invitee already exists: send notification to invitee
        if (not instance.is_inviter and instance.relation_from.created_at <
                timezone.now() - timedelta(minutes=1)):
            notifications.generic.registered_company_invite(
                instance.relation_to, instance.relation_from)
            notifications.internal.registered_company_invite(
                instance.relation_to, instance.relation_from)
        # If invitee was just created: send notification to inviter
        elif (not instance.is_inviter and instance.relation_from.created_at >
                timezone.now() - timedelta(minutes=1)):
            notifications.generic.invitation_accepted_notify_inviter(
                instance.relation_to, instance.relation_from)


def create_company_relation(inviter, invitee):
    res = CompanyRelation.objects.filter(
        relation_from=inviter, relation_to=invitee)
    # Only create relation if it doesnt already exists
    if inviter and invitee and res.count() == 0:
        inviter_relation = CompanyRelation.objects.create(
            relation_from=inviter, relation_to=invitee, is_inviter=True,
            active=True)
        invitee_relation = None
        try:
            invitee_relation = CompanyRelation.objects.create(
                relation_from=invitee, relation_to=inviter, is_inviter=False,
                active=True, sibling=inviter_relation)
            inviter_relation.sibling = invitee_relation
            inviter_relation.save()
        except Exception:
            if inviter_relation:
                inviter_relation.delete()
            if invitee_relation:
                invitee_relation.delete()


class CompanyInvite(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    inviter_user = models.ForeignKey('GenericUser', null=True, blank=True)
    inviter_company = models.ForeignKey('GenericCompany')
    invitee_name = models.CharField(max_length=200)
    invitee_email = models.EmailField()
    invitee_dot = models.IntegerField(null=True, blank=True)
    invitee_phone = models.CharField(max_length=20, blank=True, null=True)
    invitee_company_type = models.CharField(
        max_length=200, choices=CompanyType.CHOICES,
        default=CompanyType.UNKNOWN)
    invite_accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = (
            ('inviter_company', 'invitee_email'),
            ('inviter_company', 'invitee_dot'))


@receiver(pre_save, sender=CompanyInvite)
def company_invite_pre_save(sender, instance, raw, **kwargs):
    if isinstance(instance.invitee_email, basestring):
        instance.invitee_email = instance.invitee_email.lower()
        pass


@receiver(post_save, sender=CompanyInvite)
def company_invite_post_save(sender, instance, created, raw, **kwargs):
    # Create CompanyRelations if company with DOT exists
    if instance.invitee_dot:
        res = GenericCompany.objects.filter(dot=instance.invitee_dot)
        if res.count():
            create_company_relation(instance.inviter_company, res[0])
            if created:
                instance.invite_accepted = True
                instance.save()
            return True
    # Create CompanyRelations if user with email exists
    if instance.invitee_email:
        res = GenericUser.objects.filter(email=instance.invitee_email)
        if res.count():
            create_company_relation(
                instance.inviter_company, res[0].company)
            # Set DOT on instance to prevent future duplicates
            if created:
                instance.invitee_dot = res[0].company.dot
                instance.invite_accepted = True
                instance.save()
            return True


@receiver(post_save, sender=CompanyInvite)
def company_invite_post_save_notifications(
        sender, instance, created, raw, **kwargs):
    # Only send out invitations when created
    if created:
        # Check if invitee company exists
        try:
            GenericCompany.objects.exclude(dot=None).get(
                dot=instance.invitee_dot)
            return True
        except:
            pass
        try:
            GenericCompany.objects.get(email=instance.invitee_email)
            return True
        except:
            pass

        # Invite invitee to join Traansmission only if non of above checks
        # returned.
        if instance.invitee_company_type == CompanyType.SHIPPER:
            notifications.shippers.unregistered_company_invite(
                instance.inviter_company, instance.invitee_name,
                instance.invitee_email)
        elif instance.invitee_company_type == CompanyType.CARRIER:
            notifications.carriers.unregistered_company_invite(
                instance.inviter_company, instance.invitee_name,
                instance.invitee_email)
        else:
            notifications.generic.unregistered_company_invite(
                instance.inviter_company, instance.invitee_name,
                instance.invitee_email)
        notifications.internal.unregistered_company_invite(
            instance.inviter_company, instance.invitee_name,
            instance.invitee_email, instance.invitee_phone)
