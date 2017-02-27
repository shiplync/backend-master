from django.contrib.gis.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class TagCategory(object):
    # Determine category from tag:
    # category.value = ceil(tag.value / 1000)
    TRAILER = 1
    TRAILER_EXTRA = 2

    TAG_CATEGORY_CHOICES = (
        (TRAILER, 'Trailer type'),
        (TRAILER_EXTRA, 'Extra trailer equipment'),
    )


class TagType(object):
    # Trailer: 1 - 1000
    FLATBED = 1
    VAN = 2
    REEFER = 3
    POWER_ONLY = 4

    # Trailer extra: 1001 - 2000
    TARPS = 1001
    SIDES = 1002
    VENTED = 1003

    TAG_TYPE_CHOICES = (
        # Trailer
        (FLATBED, 'Flatbed'),
        (VAN, 'Van'),
        (REEFER, 'Reefer'),
        (POWER_ONLY, 'Power Only'),

        # Trailer extra
        (TARPS, 'Tarps'),
        (VENTED, 'Vented'),
    )


class EquipmentTag(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    tag_category = models.IntegerField(
        choices=TagCategory.TAG_CATEGORY_CHOICES,
        default=TagCategory.TRAILER)
    tag_type = models.IntegerField(
        choices=TagType.TAG_TYPE_CHOICES,
        default=TagType.FLATBED)
    assignee_limit = models.Q(
        models.Q(app_label='shipments', model='shipment') |
        models.Q(app_label='shipments', model='genericuser'))
    assignee_content_type = models.ForeignKey(
        ContentType, limit_choices_to=assignee_limit,
        related_name='equipment_tag_assignee')
    assignee_id = models.PositiveIntegerField()
    assignee = GenericForeignKey('assignee_content_type', 'assignee_id')
    assigner = models.ForeignKey('GenericUser', null=True, blank=True)

    @property
    def tag_category_label(self):
        return filter(
            lambda x: x[0] == self.tag_category,
            TagCategory.TAG_CATEGORY_CHOICES)[0][1]

    @property
    def tag_type_label(self):
        return filter(
            lambda x: x[0] == self.tag_type,
            TagType.TAG_TYPE_CHOICES)[0][1]

    class Meta:
        ordering = ('tag_category',)
        unique_together = (
            ('assignee_id', 'assignee_content_type',
                'tag_type', 'tag_category'),)

    def clean(self):
        ct = ContentType.objects.get(model=self.assignee_content_type)
        codename = 'change_%s' % ct.model
        if not self.assigner.user.has_perm(codename, self.assignee):
            raise ValidationError(
                _('Assigner must have permission to update assignee'))
