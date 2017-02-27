from base import notification
from django.conf import settings

def signup_approved(shipper):
    '''Welcome email to new shippers'''
    n = notification()
    n.receiver_email = shipper.owner.email
    n.receiver_name = shipper.owner.name
    n.email_subject = 'Welcome to Traansmission'

    # Email content
    n.email_content.append('Congratulations! You have made a smart choice and you now have full access to the site.')
    n.email_content.append('In case you don\'t know already, here\'s how <a href="http://www.traansmission.com" target="_blank">Traansmission</a> works:')
    n.email_content.append('Step 1: Add a shipment. Or email us if you want us to do it for you or need help. <br>Step 2: Approve interested carriers that request to move your freight. <br>Step 3: Get real-time updates on where your freight is. <br>Step 4: Get your freight delivered on time and intact.')
    n.email_content.append('With a large group of high-quality carriers, industry-leading on-time performance, and end-to-end transparency, we are already looking out for you at every turn.')
    n.email_content.append('If you have any questions, or just want to reach out, do not hesitate to call or email us: ')
    n.email_content.append('Phone: <a href="tel:+14124475623">(412)-447-5623</a> <br>Email: Connor: <a href="mailto:connor@traansmission.com" target="_blank">connor@traansmission.<wbr>com</a>, Jason: <a href="mailto:jason@traansmission.com" target="_blank">jason@traansmission.<wbr>com</a> or anyone else on the sales team at <a href="mailto:sales@traansmission.com" target="_blank">sales@traansmission.com</a>')
    n.email_content.append('The whole team is excited to be working with you!')
    n.email_content.append('Best wishes,')
    n.email_content.append('Jason Cahill <br>CEO <br>')
    # Send notifications
    n.send_all()

def signup_declined(shipper):
    '''Email notifying shipper that we could not approve their account'''
    n = notification()
    n.receiver_email = shipper.owner.email
    n.receiver_name = shipper.owner.name
    n.email_subject = 'Pending approval'

    # Email content
    n.email_content.append('Thank you for reaching out, we appreciate your interest in joining <a href="http://www.traansmission.com" target="_blank">Traansmission</a>')
    n.email_content.append('We have received an encouraging amount of support and outreach for joining the platform. Because of this, you may notice a delay in our approval process as we continue to make sure we offer the best service in the industry.')
    n.email_content.append('Please reach out to <a href="mailto:connor@traansmission.com" target="_blank"><span class="il">connor</span>@traansmission.com</a> with any questions and thank you again for your time.')
    
    # Send notifications
    n.send_all()        

def shipment_requested(shipment, shipper, carrier):
    '''Notification that a shipment was requested by a carrier'''
    n = notification()
    n.receiver_email = shipment.first_location.address_details.email if shipment.first_location.address_details.email else shipper.owner.email
    n.receiver_name = shipper.owner.name # Might need to change and reflect above email
    n.email_subject = 'Shipment %s requested' % shipment.shipment_id

    origin = shipment.first_location.address_details.city if shipment.first_location.address_details.city else shipment.first_location.address_details.address
    destination = shipment.last_location.address_details.city if shipment.last_location.address_details.city else shipment.last_location.address_details.address

    # Email content
    n.email_content.append('Hey %s,' % n.receiver_name)
    n.email_content.append('Your shipment <i>%s</i> going from <i>%s</i> to <i>%s</i> was claimed by a carrier. ' % (shipment.shipment_id, origin, destination))
    n.email_content.append('Please go to your <a href="%sshipments/shipment/%i/" target="_blank">portal</a> to approve or reject the carrier.' % (settings.PORTAL_URL, shipment.id))
    
    # Send notifications
    n.send_all()    

def shipment_enroute(shipment, shipper, carrier):
    '''Notification that a shipment was picked up (en route)'''
    n = notification()
    n.receiver_email = shipment.first_location.address_details.email if shipment.first_location.address_details.email else shipper.owner.email
    n.receiver_name = shipper.owner.name # Might need to change and reflect above email
    n.email_subject = 'Shipment %s en route update' % shipment.shipment_id

    origin = shipment.first_location.address_details.city if shipment.first_location.address_details.city else shipment.first_location.address_details.address
    destination = shipment.last_location.address_details.city if shipment.last_location.address_details.city else shipment.last_location.address_details.address

    # Email content
    n.email_content.append('Hey %s,' % n.receiver_name)
    n.email_content.append('Your shipment <i>%s</i> going from <i>%s</i> to <i>%s</i> is about to be picked up and will soon be en route.' % (shipment.shipment_id, origin, destination))
    
    # Send notifications
    n.send_all()    

def shipment_delivered(shipment, shipper, carrier):
    '''Notification that a shipment was delivered'''
    n = notification()
    n.receiver_email = shipment.first_location.address_details.email if shipment.first_location.address_details.email else shipper.owner.email
    n.receiver_name = shipper.owner.name # Might need to change and reflect above email
    n.email_subject = 'Shipment %s delivery update' % shipment.shipment_id

    origin = shipment.first_location.address_details.city if shipment.first_location.address_details.city else shipment.first_location.address_details.address
    destination = shipment.last_location.address_details.city if shipment.last_location.address_details.city else shipment.last_location.address_details.address

    # Email content
    n.email_content.append('Hey %s,' % n.receiver_name)
    n.email_content.append('Your shipment <i>%s</i> going from <i>%s</i> to <i>%s</i> is about to be delivered by the carrier, %s. ' % (shipment.shipment_id, origin, destination, carrier.owner.name))
    n.email_content.append('We appreciate you using Traansmission to move your freight, and look forward to helping you move more!')

    # Send notifications
    n.send_all()


def unregistered_company_invite(inviter_company, invitee_name, invitee_email):
    n = notification()
    n.receiver_email = invitee_email
    n.receiver_name = invitee_name
    n.email_subject = '%s has invited you to join their network on Traansmission' % inviter_company.name

    # Email content
    if invitee_name:
        n.email_content.append('Hey %s,' % invitee_name)
    else:
        n.email_content.append('Hey,')
    n.email_content.append('%s has invited you to join their shipper/broker network on Traansmission.' % inviter_company.name)
    n.email_content.append('Traansmission connects shippers/brokers to carriers and allows them to seamlessly exchange freight. It takes less than two minutes to register.')
    n.email_content.append('If you register using %s, you will see %s in your existing network of carriers. And when you\'re ready to grow even further, add your other carriers to Traansmission. You can add as many carriers as you\'d like, increasing your network.' % (invitee_email, inviter_company.name))
    n.email_content.append('<a href="%sregister/" target="_blank">Click here</a> to register.' % (settings.PORTAL_URL,))

    # Send notifications
    n.send_all()
