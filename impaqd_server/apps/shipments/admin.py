from django.contrib import admin
from django.utils.safestring import mark_safe
from solo.admin import SingletonModelAdmin
from django.core.urlresolvers import reverse
from .reverseadmin import ReverseModelAdmin

from .models import (
    Shipment, ShipmentLocation, GlobalSettings, Platform,
    ShipmentRequest, FileContext, TOSAcceptance, DemoAccount,
    GenericCompany, GenericUser, CompanyInvite, CompanyRelation,
    ShipmentAssignment, EquipmentTag, UserInvite, CompanyDivision,
    CompanyDivisionMembership, SavedLocation, ShipmentCarrierAssignment,
    ShipmentDriverAssignment)
admin.autodiscover()


class EditLinkToInlineObject(object):
    def edit_link(self, instance):
        url = reverse('admin:%s_%s_change' % (
            instance._meta.app_label,
            instance._meta.model_name),
            args=(instance.pk,))
        if instance.pk:
            return mark_safe(u'<a href="{u}">Edit here</a>'.format(u=url))
        else:
            return ''


class ShipmentLocationAdmin(ReverseModelAdmin):
    inline_type = 'stacked'
    inline_reverse = ('contact', 'address_details', 'time_range', 'features',)


class ShipmentLocationInline(EditLinkToInlineObject, admin.StackedInline):
    model = ShipmentLocation
    extra = 0
    readonly_fields = (
        'edit_link', 'company_name', 'dock', 'appointment_id',
        'comments', 'saved', 'arrival_time', 'contact', 'features',
        'time_range', 'address_details', 'next_location',
        'distance_to_next_location', 'latitude', 'longitude',)


class ShipmentAdmin(ReverseModelAdmin):
    inline_type = 'stacked'
    inline_reverse = ('payout_info',)
    list_display = (
        'owner', 'created_at', 'carrier', 'carrier_is_approved',
        'first_location', 'last_location', 'location_count',
        'delivery_status',)
    readonly_fields = ('first_location', 'last_location', 'trip_distance',)
    inlines = (ShipmentLocationInline,)


def allow_notifications(modeladmin, request, queryset):
    queryset.update(allow_notifications=True)
allow_notifications.short_description = \
    "Allow notifications for selected carriers"


def disallow_notifications(modeladmin, request, queryset):
    queryset.update(allow_notifications=False)
disallow_notifications.short_description = \
    "Disallow notifications for selected carriers"


class PlatformInline(admin.TabularInline):
    model = Platform
    extra = 1


class GenericUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'company', 'user_type', 'created_at',)

    def profile_photo_view(self, instance):
        if instance.profile_photo:
            return mark_safe(
                '<img src="%s">' % instance.profile_photo.file_url)
        else:
            return ''
    profile_photo_view.short_description = 'Profile photo'

    def photo_image_raw(self, instance):
        if instance:
            clean_base64 = instance.photo.replace('\r', '').replace('\n', '')
            return mark_safe(
                '<img height="180px" alt="Photo" '
                'src="data:image/jpeg;base64,%s"' % clean_base64)
        return ''
    readonly_fields = (
        'created_at', 'profile_photo_view', 'photo_image_raw',
        'tos_acceptance',)
    # display the photo, which is a base64-encoded JPEG, but don't allow direct
    # access to the data
    exclude = ('photo',)
    inlines = (PlatformInline,)


class ShipmentRequestAdmin(admin.ModelAdmin):
    readonly_fields = ('shipment', 'carrier',)


class FileContextAdmin(admin.ModelAdmin):
    readonly_fields = (
        'file_url', 'uuid_value', 'path', 'created_at', 'updated_at',)


class TOSAcceptanceAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'tos_status', 'tos_version',)
    readonly_fields = ('created_at', 'tos_updated_at')


class PlatformAdmin(admin.ModelAdmin):
    list_display = ('user', 'platform_type',)


class DemoAccountAdmin(admin.ModelAdmin):
    pass


class GenericCompanyAdmin(admin.ModelAdmin):
    list_display = (
        'company_name', 'company_type', 'owner', 'dot', 'verified', 'rejected',
        'created_at')
    readonly_fields = ('created_at', 'remaining_user_invites',)


class CompanyRelationAdmin(admin.ModelAdmin):
    list_display = ('id', 'relation_from', 'relation_to', 'created_at')


class CompanyInviteAdmin(admin.ModelAdmin):
    list_display = (
        'invitee_email', 'invitee_dot', 'invitee_name', 'invitee_company_type',
        'inviter_user', 'inviter_company', 'invite_accepted', 'created_at',)


class UserInviteAdmin(admin.ModelAdmin):
    list_display = (
        'email', 'company', 'first_name', 'last_name', 'user', 'user_type',
        'active')


class ShipmentAssignmentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'assignee', 'assignee_content_type', 'shipment', 'created_at')


class EquipmentTagAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'assignee', 'assignee_content_type', 'tag_type', 'tag_category',
        'created_at')


class CompanyDivisionAdmin(admin.ModelAdmin):
    list_display = ('company', 'name',)


class CompanyDivisionMembershipAdmin(admin.ModelAdmin):
    list_display = ('division', 'user',)


class SavedLocationAdmin(ReverseModelAdmin):
    inline_type = 'stacked'
    inline_reverse = ('contact', 'address_details',)
    list_display = ('id', 'company_name', 'owner',)


class ShipmentCarrierAssignmentAdmin(ReverseModelAdmin):
    inline_type = 'stacked'
    inline_reverse = ('assignment',)
    list_display = ('assignment',)


class ShipmentDriverAssignmentAdmin(ReverseModelAdmin):
    inline_type = 'stacked'
    inline_reverse = ('assignment',)
    list_display = ('assignment',)


admin.site.register(Shipment, ShipmentAdmin)
admin.site.register(GlobalSettings, SingletonModelAdmin)
admin.site.register(GenericUser, GenericUserAdmin)
admin.site.register(ShipmentRequest, ShipmentRequestAdmin)
admin.site.register(FileContext, FileContextAdmin)
admin.site.register(TOSAcceptance, TOSAcceptanceAdmin)
admin.site.register(Platform, PlatformAdmin)
admin.site.register(DemoAccount, DemoAccountAdmin)
admin.site.register(GenericCompany, GenericCompanyAdmin)
admin.site.register(CompanyRelation, CompanyRelationAdmin)
admin.site.register(CompanyInvite, CompanyInviteAdmin)
admin.site.register(ShipmentAssignment, ShipmentAssignmentAdmin)
admin.site.register(EquipmentTag, EquipmentTagAdmin)
admin.site.register(ShipmentLocation, ShipmentLocationAdmin)
admin.site.register(UserInvite, UserInviteAdmin)
admin.site.register(CompanyDivision, CompanyDivisionAdmin)
admin.site.register(CompanyDivisionMembership, CompanyDivisionMembershipAdmin)
admin.site.register(SavedLocation, SavedLocationAdmin)
admin.site.register(ShipmentCarrierAssignment, ShipmentCarrierAssignmentAdmin)
admin.site.register(ShipmentDriverAssignment, ShipmentDriverAssignmentAdmin)
