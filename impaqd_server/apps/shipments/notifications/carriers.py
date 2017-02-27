from base import notification
from django.conf import settings

def signup_approved(carrier):
    '''Welcome email to new carriers'''
    n = notification()
    n.receiver_email = carrier.owner.email
    n.receiver_name = carrier.owner.name
    n.email_subject = 'Welcome to Traansmission'

    # Email content
    n.email_content.append('Success! You have been approved. You can now fully use the <a href="http://www.traansmission.com" target="_blank">website</a> and the <a href="https://itunes.apple.com/us/app/traansmission/id833771825" target="_blank">iOS</a>/<a href="https://play.google.com/store/apps/details?id=com.traansmission&amp;hl=en" target="_blank">Android</a> mobile app.')
    n.email_content.append('Shoot us an <a href="mailto:sales@traansmission.com" target="_blank">email</a> with your preferred lanes so we can get you loaded.')
    
    # Send notifications
    n.send_all()

def signup_declined(carrier):
    '''Email notifying carrier that we could not approve their account'''
    n = notification()
    n.receiver_email = carrier.owner.email
    n.receiver_name = carrier.owner.name
    n.email_subject = 'Pending approval'

    # Email content
    n.email_content.append('Thank you for reaching out, we appreciate your interest in joining <a href="http://www.traansmission.com" target="_blank">Traansmission</a>')
    n.email_content.append('We have received an encouraging amount of support and outreach for joining the platform. Because of this, you may notice a delay in our approval process as we continue to make sure we offer the best service in the industry.')
    n.email_content.append('Please reach out to <a href="mailto:connor@traansmission.com" target="_blank">connor@traansmission.<wbr>com</a> with any questions and thank you again for your time.')
    
    # Send notifications
    n.send_all()    

def request_approved(shipment, shipper, carrier):
    '''Notification that a shipment request was approved'''
    n = notification()
    n.receiver_email = carrier.owner.email
    n.receiver_name = carrier.owner.name
    n.email_subject = 'Request approved'

    # Email content
    n.email_content.append('Hey %s,' % carrier.owner.name)
    n.email_content.append('Your request for shipment <i>%s</i> has been approved.' % shipment.shipment_id)
    n.email_content.append('Please stand by as we contact you with shipment instructions.') 
    
    # Send notifications
    n.send_all()

def request_declined(shipment, shipper, carrier):
    '''Notification that a shipment request was declined'''
    n = notification()
    n.receiver_email = carrier.owner.email
    n.receiver_name = carrier.owner.name
    n.email_subject = 'Request declined'

    # Email content
    n.email_content.append('Hey %s,' % carrier.owner.name)
    n.email_content.append('Unfortunately, your request for shipment <i>%s</i> was declined. Feel free to contact us directly if you have any questions.' % shipment.shipment_id)

    # Send notifications
    n.send_all()


def unregistered_company_invite(inviter_company, invitee_name, invitee_email):
    n = notification()
    n.receiver_email = invitee_email
    n.receiver_name = invitee_name
    n.email_subject = (
        '%s has invited you to join their network on Traansmission' %
        inviter_company.name)

    # Email content
    if invitee_name:
        n.email_content.append('Hey %s,' % invitee_name)
    else:
        n.email_content.append('Hey,')
    n.email_content.append(
        '%s has invited you to join their carrier network on Traansmission.' %
        inviter_company.name)
    n.email_content.append(
        'Traansmission is a transportation management system that connects '
        'carriers and shippers/brokers to seamlessly exchange freight. '
        'Traansmission manages your freight contacts and schedules and every '
        'load can be enabled with track and trace using our mobile app.')
    n.email_content.append(
        '<b>It takes two minutes to register and Traansmission is always free '
        'to use for carriers.</b>')
    n.email_content.append(
        'When registering, use %s, to see %s in your existing network of '
        'shippers/brokers. To grow even further, add your other brokers to '
        'Traansmission.' % (invitee_email, inviter_company.name))
    n.email_content.append(
        'Add as many brokers as you\'d like, to grow your freight network. '
        '<b><a href="%sregister/" target="_blank">Click here</a> to '
        'register.</b>' % (settings.PORTAL_URL,))

    # Send notifications
    n.send_all()


def shipment_assigned_carrier(
        assigner_company, assignee_company, shipment, assignee_user=None):
    n = notification()
    if assignee_user:
        assignee_email = assignee_user.email
        assignee_name = assignee_user.name
    else:
        assignee_email = assignee_company.owner.email
        assignee_name = assignee_company.company_name

    n.receiver_email = assignee_email
    n.receiver_name = assignee_name
    assigner_name = (
        assigner_company.company_name if assigner_company.company_name else
        assigner_company.owner.name)
    n.email_subject = 'New shipment!'

    # Email content
    n.email_content.append(
        '%s has shared a shipment with you going from %s, %s to %s, %s' %
        (assigner_name, 
            shipment.first_location.address_details.city,
            shipment.first_location.address_details.state,
            shipment.last_location.address_details.city, 
            shipment.last_location.address_details.state))
    n.email_content.append(
        'You can request it <a href="%sshipments/shipment/%i" '
        'target="_blank">directly from the portal</a> or from the carrier '
        'iOS/Android app' % (settings.PORTAL_URL, shipment.id))
    # Send notifications
    n.send_all()
