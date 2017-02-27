from base import internalNotification


def shipment_posted(shipment, shipper):
    '''Notification about a shipment was posted'''
    n = internalNotification()
    n.email_subject = 'New shipment posted'

    # Email content
    n.email_content.append('Shipper/broker <i>%s</i> posted a new shipment with id <i>%s</i>.' % (shipper.company_name, shipment.shipment_id))
    
    # Send notifications
    n.send_all()

def shipment_requested(shipment, shipper, carrier):
    '''Notification about a shipment was requested'''
    n = internalNotification()
    n.email_subject = 'Shipment requested'

    # Email content
    n.email_content.append('Shipment <i>%s</i> posted by <i>%s</i> was requested by the carrier <i>%s</i>.' % (shipment.shipment_id, shipper.company_name, carrier.owner.name))
    
    # Send notifications
    n.send_all()    

def shipment_enroute(shipment, shipper, carrier):
    '''Notification about a shipment is en route'''
    n = internalNotification()
    n.email_subject = 'Shipment picked up'

    # Email content
    n.email_content.append('Shipment <i>%s</i> posted by <i>%s</i> was picked up by the carrier <i>%s</i>.' % (shipment.shipment_id, shipper.company_name, carrier.owner.name))
    
    # Send notifications
    n.send_all()    

def shipment_delivered(shipment, shipper, carrier):
    '''Notification about a shipment being delivered'''
    n = internalNotification()
    n.email_subject = 'Shipment delivered'

    # Email content
    n.email_content.append('Shipment <i>%s</i> posted by <i>%s</i> was delivered by the carrier <i>%s</i>.' % (shipment.shipment_id, shipper.company_name, carrier.owner.name))
    
    # Send notifications
    n.send_all()        


def request_approved(shipment, shipper, carrier):
    '''Notification about a shipment request was approved'''
    n = internalNotification()
    n.email_subject = 'Shipment request approved'

    # Email content
    n.email_content.append('Shipper/broker <i>%s</i> has approved  carrier <i>%s</i> for shipment <i>%s</i>.' % (shipper.company_name, carrier.owner.name, shipment.shipment_id))
    
    # Send notifications
    n.send_all()    

def request_declined(shipment, shipper, carrier):
    '''Notification about a shipment request was declined'''
    n = internalNotification()
    n.email_subject = 'Shipment request declined'

    # Email content
    n.email_content.append('Shipper/broker <i>%s</i> has declined  carrier <i>%s</i> for shipment <i>%s</i>.' % (shipper.company_name, carrier.owner.name, shipment.shipment_id))
    
    # Send notifications
    n.send_all()    

def test():
    n = internalNotification()
    n.email_subject = 'Test'

    # Email content
    n.email_content.append('Test')

    # Send notifications
    n.send_all()    


def registered_company_invite(inviter_company, invitee_company):
    n = internalNotification()
    inviter_name = (
        inviter_company.company_name if inviter_company.company_name else
        inviter_company.owner.name)
    invitee_name = (
        invitee_company.company_name if invitee_company.company_name else
        invitee_company.owner.name)
    n.email_subject = '%s has added a new company to their network' % inviter_name

    # Email content
    n.email_content.append('%s and %s are now connected on Traansmission.' % (inviter_name, invitee_name))

    # Send notifications
    n.send_all()


def unregistered_company_invite(
        inviter_company, invitee_name, invitee_email, invitee_phone):
    n = internalNotification()
    inviter_name = (
        inviter_company.company_name if inviter_company.company_name else
        inviter_company.owner.name)
    n.email_subject = '%s has invited a company to join Traansmission' % inviter_name

    # Email content
    n.email_content.append('%s has invited %s to join Traansmission.' % (inviter_name, (invitee_name if invitee_name else invitee_email)))
    n.email_content.append('Do not forget to follow up with invited company!')
    n.email_content.append('Email: %s' % invitee_email)
    if invitee_phone:
        n.email_content.append('Phone: %s' % invitee_phone)


    # Send notifications
    n.send_all()


def shipment_assigned_carrier(
        assigner_company, assignee_company, shipment, assignee_user=None):
    n = internalNotification()
    if assignee_user:
        assignee_name = assignee_user.name
    else:
        assignee_name = assignee_company.company_name

    assigner_name = (
        assigner_company.company_name if assigner_company.company_name else
        assigner_company.owner.name)
    n.email_subject = (
        '%s shared a shipment with %s' % (assigner_name, assignee_name))

    # Email content
    n.email_content.append(
        '%s has shared a shipment with %s going from %s, %s to %s, %s' %
        (assigner_name, assignee_name, shipment.first_location.address_details.city,
            shipment.first_location.address_details.state, shipment.last_location.address_details.city,
            shipment.last_location.address_details.state))

    # Send notifications
    n.send_all()


def auto_verify_company(company, inviter):
    n = internalNotification()
    n.email_subject = (
        '%s has signed up and been verified' % company.name)

    # Email content
    n.email_content.append(
        '%s, invited by %s, has automatically been verified' % (
            company.name, inviter.name))

    # Send notifications
    n.send_all()
