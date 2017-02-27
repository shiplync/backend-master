import time
from apns import APNs, Payload
import os
import re
from ssl import SSLError
from django.conf import settings
from .models import GenericCompany, CompanyType
from .models.shipments import PlatformType

import logging
LOG = logging.getLogger('impaqd')

module_dir = os.path.dirname(__file__)  # get current directory
file_path = os.path.join(module_dir, 'certificates')
certificate_type = settings.CERTIFICATE

def pushLoadSingleCarrier(carrier, shipment):
    '''Push to all Apple devices
    '''
    shipment_id = shipment.id
    custom = {'shipment_id': shipment_id, 'type':'single-load-rec'}
    print str(round(shipment.payout_mile, 2))
    alert = "There's a new shipment going from " + shipment.first_location.address_details.city + ", " + shipment.first_location.address_details.state + " to " + shipment.last_location.address_details.city + ", " + shipment.last_location.address_details.state + " at a price of $" + str("%.2f" % shipment.payout)
    LOG.warning(alert)
    print alert
    badge = 0
    pushNotificationAppleDevice(carrier,alert,custom,badge)

    '''Push to all Android devices
    '''
    # TO-DO: Push to Android devices

def pushLoadAllCarriers(shipment):
    carriers = GenericCompany.objects.filter(company_type=CompanyType.CARRIER)
    for carrier in carriers:
        try:
            pushLoadSingleCarrier(carrier, shipment)
        except SSLError, e:
            LOG.error(traceback.format_exc())
            print "Unable to push load to carrier: " + carrier.email


def pushShipmentHandshakeApproved(shipment, carrier, shipper):
    '''Push to all Apple devices
    '''
    shipment_id = shipment.id
    custom = {'shipment_id': shipment_id, 'type':'load-request-approved'}
    alert = "Your request has been approved!"
    badge = 0
    pushNotificationAppleDevice(carrier,alert,custom,badge)

    '''Push to all Android devices
    '''
    # TO-DO: Push to Android devices

def pushShipmentHandshakeDeclined(shipment, carrier, shipper):  
    '''Push to all Apple devices
    '''
    shipment_id = shipment.id
    custom = {'shipment_id': shipment_id, 'type':'load-request-declined'}
    alert = "Sorry, your request was declined by the shipper"
    badge = 0
    pushNotificationAppleDevice(carrier,alert,custom,badge)

    '''Push to all Android devices
    '''
    # TO-DO: Push to Android devices


def pushNotificationAppleDevice(carrier, alert, custom, badge):
    ios_set = carrier.owner.platform_set.filter(platform_type=PlatformType.IOS)
    for s in ios_set:
        if s.allow_notifications:
            try:
                token = re.sub('[ <>]', '', s.identifier)
                if certificate_type == 'prod':
                    apns = APNs(use_sandbox=False, cert_file=file_path + '/prod/pushprod.pem', key_file=file_path + '/prod/ImpaqdPushProd.pem')
                elif certificate_type == 'dev':
                    apns = APNs(use_sandbox=True, cert_file=file_path + '/dev/pushdev.pem', key_file=file_path + '/dev/ImpaqdPushDev.pem')
                elif certificate_type == 'demo-prod':
                    apns = APNs(use_sandbox=False, cert_file=file_path + '/demoProd/pushdemoprod.pem', key_file=file_path + '/demoProd/ImpaqdDemoPushProd.pem') 
                elif certificate_type == 'demo-dev':
                    apns = APNs(use_sandbox=True, cert_file=file_path + '/demoDev/pushdemodev.pem', key_file=file_path + '/demoDev/ImpaqdDemoPushDev.pem')
                elif certificate_type == 'sandbox-prod':
                    apns = APNs(use_sandbox=False, cert_file=file_path + '/sandboxProd/pushsandboxprod.pem', key_file=file_path + '/sandboxProd/ImpaqdSandboxPushProd.pem') 
                elif certificate_type == 'sandbox-dev':
                    apns = APNs(use_sandbox=True, cert_file=file_path + '/sandboxDev/pushsandboxdev.pem', key_file=file_path + '/sandboxDev/ImpaqdSandboxPushDev.pem')
                else:
                    print 'NO CERTIFICATE CHOSEN (set value in secrets.py)'
                # Type can be: single-load-rec, load-request-approved, load-request-declined
                payload = Payload(alert=alert, sound="default", badge=badge, custom=custom)
                apns.gateway_server.send_notification(token, payload)
            except Exception, e:
                LOG.error(traceback.format_exc())
                print 'Unable to send push notification to ' + carrier.owner.email
