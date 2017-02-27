from django.contrib import admin
from .models.notifications import Notification
from .models.user_invite import UserInviteNotif
from .models.signup_internal import SignupInternalNotif
from .models.retention import (
    Day1, Day7, Day15, Day28, Day31, Day38)


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('parent_content_type', 'created_at', 'receiver_email',)


admin.site.register(Notification, NotificationAdmin)
admin.site.register(UserInviteNotif)
admin.site.register(SignupInternalNotif)
admin.site.register(Day1)
admin.site.register(Day7)
admin.site.register(Day15)
admin.site.register(Day28)
admin.site.register(Day31)
admin.site.register(Day38)
