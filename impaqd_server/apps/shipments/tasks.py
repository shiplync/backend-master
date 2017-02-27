from __future__ import absolute_import

from django.contrib.gis.geos import Point
from celery import shared_task
from .models.generic_user import GenericUser
from .models.generic_company import GenericCompany, CompanyType
from .models.relations import CompanyInvite, create_company_relation
from .utils import reverse_geocode, get_trip_dist
from ..notifications.models.signup_internal import SignupInternalNotif
from ..notifications.models.retention import Day1

"""
Must import signals to connect them
TODO: Use "Signal.connect()" instead
"""
from .models.relations import company_relation_post_save
from .models.locations import (
    shipmentlocation_created_update_shipment,
    shipmentlocation_deleted_update_shipment,
    timerange_update_shipment)


@shared_task
def pushLoadAllCarriersTask(shipment):
    from .pushNotifications import pushLoadAllCarriers
    pushLoadAllCarriers(shipment)


@shared_task
def worker_test_task():
    return True


@shared_task(ignore_result=True)
def task_update_carrier_driver_geolocation(geolocation):
    driver = geolocation.driver
    GenericUser.objects.filter(pk=driver.pk).update(
        last_location=Point(geolocation.latitude, geolocation.longitude),
        last_location_timestamp=geolocation.timestamp)


@shared_task(ignore_result=True)
def task_update_shipment_tracking_geolocation(geolocation):
    pass
    return True


@shared_task(ignore_result=True)
def task_update_geolocation_display_text(geolocation):
    display_text = reverse_geocode(geolocation.longitude, geolocation.latitude)
    if display_text:
        geolocation.display_text = display_text
        geolocation.save()


@shared_task(ignore_result=True)
def task_new_user_or_company_create_company_relations(company_or_user):
    # Look for invite based on DOT
    if company_or_user.__class__ == GenericCompany and company_or_user.dot:
        company = company_or_user
        res = CompanyInvite.objects.filter(invitee_dot=company.dot)
        if res.count():
            invite = res[0]
            create_company_relation(invite.inviter_company, company)
            invite.invite_accepted = True
            invite.save()
    # Look for invite based on user email
    elif company_or_user.__class__ == GenericUser:
        user = company_or_user
        res = CompanyInvite.objects.filter(invitee_email=user.email)
        if res.count():
            invite = res[0]
            create_company_relation(invite.inviter_company, user.company)
            invite.invite_accepted = True
            if user.company.dot:
                invite.invitee_dot = user.company.dot
            invite.save()


@shared_task(ignore_result=True)
def task_new_company_handle_verification(company):
    from impaqd_server.apps.shipments import notifications
    # Check if company was invited by another company
    inviter = None
    try:
        inviter = CompanyInvite.objects.filter(
            invitee_email=company.owner.email)[0].inviter_company
    except:
        pass
    if not inviter:
        try:
            inviter = CompanyInvite.objects.exclude(invitee_dot=None).filter(
                invitee_dot=company.dot)[0].inviter_company
        except:
            pass
    if inviter:
        pass
        # Company was invited: Auto verify company.
        # Good practice not to use "save()" in async task
        # GenericCompany.objects.filter(pk=company.id).update(
        #     verified=True)
        # if company.company_type == CompanyType.CARRIER:
        #     notifications.carriers.signup_approved(company)
        # elif company.company_type == CompanyType.SHIPPER:
        #     notifications.shippers.signup_approved(company)
        # notifications.internal.auto_verify_company(company, inviter)
    else:
        # Company was not invited: Send out internal pending verification email
        SignupInternalNotif.objects.create(company=company)
        # c_type = filter(
        #     lambda x: x[0] == company.company_type, CompanyType.CHOICES)[0][1]
        # notifications.custom.signup_internal(
        #     company.owner.email, company.owner.name, str(company.owner.phone),
        #     c_type, company.company_name, company.dot, company.pk)

    # Send welcome email
    Day1.objects.create(receiver=company.owner)


# @shared_task(ignore_result=True)
# def task_update_trip_distance(shipment):
#     # Update distance_to_next_location on all locations
#     for location in shipment.locations.all():
#         if location.next_location:
#             try:
#                 distance = get_trip_dist(
#                     location.address_details.coordinate.x,
#                     location.address_details.coordinate.y,
#                     location.next_location.address_details.coordinate.x,
#                     location.next_location.address_details.coordinate.y)
#                 location.distance_to_next_location = distance
#                 location.save()
#             except Exception:
#                 pass
