from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from impaqd_server.apps.shipments.views import *
from impaqd_server.apps.shipments.views.users import UsersListView
from .apps.shipments.views.shipments import shipment_geolocations_list_view
from .apps.geolocations.views import (
    GeolocationsCreateView, CachedCoordinateViewSet, CachedDistanceViewSet)
from .apps.payments.views import SubscriptionSelfView
from .apps.permissions.views import PermissionRetrieveView

"""View sets"""
router = routers.SimpleRouter()
# Carriers
# Deprecated. Use /carriers/shipments/
router.register(r'^carriers/shipments/temp', ShipmentViewSet)
router.register(r'^carriers/requests', CarrierRequestView)

# Shippers
router.register(r'^locations', LocationBelongToShipperView)
router.register(r'^templatelocations', SavedLocationViewSet)

# Other
router.register(r'^platforms', PlatformView)
router.register(r'^shipments', ShipmentViewSet)
router.register(r'^companyinvites', CompanyInviteViewSet)
router.register(r'^shipmentassignments', ShipmentAssignmentViewSet)
router.register(r'^equipmenttags', EquipmentTagViewSet)
router.register(r'^cachedcoordinates', CachedCoordinateViewSet)
router.register(r'^cacheddistances', CachedDistanceViewSet)
router.register(r'^userinvites/accept', UserInviteAcceptViewSet)
router.register(r'^userinvites', UserInviteViewSet)
router.register(r'^divisions', CompanyDivisionViewSet)
router.register(r'^divisionmemberships', CompanyDivisionMembershipViewSet)
router.register(r'^team/users', UserTeamViewSet)
router.register(r'^team/companies', CompanyTeamViewSet)
router.register(r'^carrierassignments', ShipmentCarrierAssignmentViewSet)
router.register(r'^driverassignments', ShipmentDriverAssignmentViewSet)

"""Generic views"""
api_urlpatterns = router.urls
api_urlpatterns += patterns(
    '',

    # Carriers
    url(r'^carriers/shipments/(?P<pk>\d+)/$',
        CarrierShipmentsSingleView.as_view()),
    url(r'^carriers/status/$', CarrierVerificationView.as_view()),
    url(r'^carriers/(?P<pk>\d+)/verify/(?P<send_email>\d+)/$', verify_company),
    url(r'^carriers/(?P<pk>\d+)/reject/(?P<send_email>\d+)/$', reject_company),
    url(r'^carriers/register/$', register_carrier,
        name='carriers_register'),

    # Shippers
    url(r'^shippers/(?P<pk>\d+)/verify/(?P<send_email>\d+)/$', verify_company),
    url(r'^shippers/(?P<pk>\d+)/reject/(?P<send_email>\d+)/$', reject_company),
    url(r'^shippers/register/$', register_shipper, name='shippers_register'),
    url(r'^shippers/approve_carrier/$', shipperApproveCarrier),

    # Shipments
    url(r'^shipments/(?P<pk>\d+)/geolocations/$',
        shipment_geolocations_list_view,
        name='shipment_geolocations_list_view'),
    url(r'^shipments/(?P<pk>\d+)/updatecachedcoordinates/$',
        shipment_update_cached_coordinates),
    url(r'^shipments/(?P<pk>\d+)/updatecacheddistances/$',
        shipment_update_cached_distances),

    # User and authentication
    # DEPRECATED! use users/verify_token/ instead
    url(r'^verify_token/$', verify_token),

    # Users
    url(r'^users/self/', UsersSelfView.as_view()),
    url(r'^users/reset_password/$', reset_password),
    url(r'^users/change_password/$', change_password),
    url(r'^users/verify_token/$', verify_token),
    url(r'^users/', UsersListView.as_view(), name='users_list_view'),

    # Geolocations endpoint
    # POST only endpoint
    url(r'^geolocations/', GeolocationsCreateView.as_view(),
        name='geolocations_create_view'),

    # Companies
    url(r'^companies/self/', CompaniesSelfView.as_view()),
    url(r'^companies/related/(?P<pk>\d+)/$',
        RelatedCompaniesRetrieveUpdateView.as_view()),
    url(r'^companies/related/', RelatedCompaniesListView.as_view()),

    # Subscription
    url(r'^subscription/self/', SubscriptionSelfView.as_view()),

    # Register
    url(r'^register/$', register_company_and_user, name="company_register"),
    url(r'^register/companies/self/', RegisterCompaniesSelfView.as_view()),
    url(r'^register/subscriptions/self/',
        RegisterSubscriptionSelfView.as_view()),

    # Other
    url(r'^login/$', login),
    url(r'^logout/$', logout),
    url(r'^check_version/(?P<version>\d+(\.\d+)+)/$', check_apple_version),
    url(r'^check_android_version/(?P<version>\d+)/$', check_android_version),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^tests/worker_test/$', worker_test),
    url(r'^files/$', FileUploadView.as_view()),
    url(r'^tos/$', TOSAcceptanceView.as_view()),
    url(r'^permissions/$', PermissionRetrieveView.as_view()),
    url(r'^verification/(?P<pk>\d+)/verify/(?P<send_email>\d+)/$',
        verify_company),
    url(r'^verification/(?P<pk>\d+)/reject/(?P<send_email>\d+)/$',
        reject_company),
)
api_urlpatterns = format_suffix_patterns(api_urlpatterns)


"""URL patterns"""
urlpatterns = patterns(
    '',

    # General
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(api_urlpatterns)),

    # For password reset
    url(r'^user/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'post_reset_redirect': '/user/password/done/',
            'template_name': 'passwords/password_reset_confirm.html'},
        name='password_reset_confirm'),
    url(r'^user/password/reset/done/$',
        'django.contrib.auth.views.password_reset_done',
        name='password_reset_done'),
    url(r'^user/password/done/$',
        'django.contrib.auth.views.password_reset_complete',
        {'template_name': 'passwords/password_reset_complete.html'},
        name='password_reset_done'),
)

# support media files in DEBUG mode
from django.conf import settings
if settings.DEBUG:
    urlpatterns += patterns(
        '',
        (r'^media/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}))
