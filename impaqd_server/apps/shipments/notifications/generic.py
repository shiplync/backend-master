from django.conf import settings
from base import notification


def registered_company_invite(inviter_company, invitee_company):
    n = notification()
    n.receiver_email = invitee_company.owner.email
    n.receiver_name = invitee_company.name
    n.email_subject = (
        '%s has added you to their network on Traansmission' %
        inviter_company.name)

    # Email content
    n.email_content.append(
        '%s and %s are now connected on Traansmission.' %
        (invitee_company.name, inviter_company.name))

    # Send notifications
    n.send_all()


def invitation_accepted_notify_inviter(inviter_company, invitee_company):
    n = notification()

    n.receiver_email = inviter_company.owner.email
    n.receiver_name = inviter_company.name

    n.email_subject = (
        '%s has accepted your invitation to connect' % invitee_company.name)

    # Email content
    n.email_content.append(
        '%s and %s are now connected on Traansmission.' %
        (inviter_company.name, invitee_company.name))

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
        '<b>It only takes two minutes to register. </b>')
    n.email_content.append(
        'When registering, use %s, to see %s in your existing network of '
        'companies. ' % (invitee_email, inviter_company.name))
    n.email_content.append(
        'Add as many connections as you\'d like, to grow your freight network. '
        '<b><a href="%sregister/" target="_blank">Click here</a> to '
        'register.</b>' % (settings.PORTAL_URL,))

    # Send notifications
    n.send_all()
