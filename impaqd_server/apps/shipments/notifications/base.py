import os
from django.conf import settings
from django.core.mail import EmailMultiAlternatives


class notification:

    # Email specific properties
    receiver_email = None
    receiver_name = None
    sender_email = 'notifications@traansmission.com'
    sender_name = 'Traansmission'
    reply_to_email = settings.NOTIFICATION_EMAIL
    email_subject = None
    email_content = None

    def __init__(self):
        self.email_content = []

    def send_email(self):
        try:
            email_content_html = ''
            file_path = os.path.join(
                settings.BASE_DIR,
                'apps/notifications/templates/core/email_template.html')
            with open(file_path, 'rU') as f:
                email_content_html = f.read().replace('\n', '')
            section_wrap = '''<tr style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif; box-sizing: border-box; font-size: 14px; margin: 0; padding: 0;"><td class="content-block" style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 20px;" valign="top">%s</td></tr>'''
            html_string = ''
            for p in self.email_content:
                html_string += section_wrap % p
            email_content_html = email_content_html.replace(
                '*|email_content|*', html_string)
            msg = EmailMultiAlternatives(
                subject=self.email_subject,
                from_email=self.sender_email,
                headers={'Reply-To': settings.NOTIFICATION_EMAIL},
                to=[self.receiver_email])
            msg.attach_alternative(email_content_html, "text/html")
            msg.send()
        except Exception, e:
            print "Unable to send email"
            print str(e)

#         try:                     
#             content_string = ''
#             for p in self.email_content:
#                 content_string += '''<tr style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif; box-sizing: border-box; font-size: 14px; margin: 0; padding: 0;"><td class="content-block" style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 20px;" valign="top">%s</td></tr>''' % p
# 
#             msg = EmailMessage(subject=self.email_subject, from_email=self.sender_email, headers={'Reply-To': self.reply_to_email}, to=[self.receiver_email,])
#             msg.template_name = 'customEmail'
#             msg.async = True
#             msg.from_name = self.sender_name
#             msg.metadata = {'website': 'www.traansmission.com'}
#             msg.global_merge_vars = { 
#                 'email_content': content_string
#             }
#             msg.send()
#         except Exception, e:
#             print "Unable to send email"
#             print str(e)
# 
#     def send_ios_push(self): 
#         # TODO
#         pass

    def send_all(self):
        if self.receiver_email and self.receiver_name and self.email_subject and self.email_content:
            print 'Sending email'
            self.send_email()
        # if ...    
            # print 'Sending ios push'
            #self.send_ios_push()


class internalNotification(notification):

    # Email specific properties
    receiver_email = settings.NOTIFICATION_EMAIL
    receiver_name = 'Traansmission'
    sender_email = 'notifications@traansmission.com'
    sender_name = 'Traansmission notifier'
    reply_to_email = 'tech@traansmission.com'

    def __init__(self):
        self.email_content = ['<b>INTERNAL NOTIFICATION</b><br><b>DOMAIN:</b> %s' % settings.PORTAL_URL]
