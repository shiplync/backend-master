from django.contrib import admin
from .models import BasePermission, BasePermissionCollection


class BasePermissionInline(admin.TabularInline):
    model = BasePermission
    exclude = ('permission',)
    readonly_fields = ('name',)


class BasePermissionCollectionAdmin(admin.ModelAdmin):
    list_display = ('genericuser',)
    readonly_fields = ('user_type',)
    inlines = (BasePermissionInline,)


class BasePermissionAdmin(admin.ModelAdmin):
    model = BasePermission
    list_display = ('name', 'permission_collection')


admin.site.register(BasePermissionCollection, BasePermissionCollectionAdmin)
admin.site.register(BasePermission, BasePermissionAdmin)
