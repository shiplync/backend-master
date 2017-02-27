from django.contrib import admin
from .models import Geolocation, CachedCoordinate, CachedDistance

admin.autodiscover()


class GeolocationAdmin(admin.ModelAdmin):
    list_display = ('driver', 'timestamp', 'shipment',)


class CachedCoordinateAdmin(admin.ModelAdmin):
    pass


class CachedDistanceAdmin(admin.ModelAdmin):
    pass


admin.site.register(Geolocation, GeolocationAdmin)
admin.site.register(CachedCoordinate, CachedCoordinateAdmin)
admin.site.register(CachedDistance, CachedDistanceAdmin)
