from django.conf import settings
import requests
from django.core.mail import EmailMessage


# def signup_internal(_email, _name, _phone, _company_type, _company, _dot, _id):
#     '''Send internal notification email that a carrier has signed up.
#     Email includes actions that allows us to verify/reject the request.
#     '''
#     receiver_email = settings.NOTIFICATION_EMAIL
#     sender_email = 'notifications@traansmission.com'
#     sender_name = 'Traansmission notifier'
#     reply_to_email = 'tech@traansmission.com'
#     email_subject = _company_type + ' needs verification'
#     dot_record = ''
#     if _dot:
#         try:
#             url = 'http://safer.fmcsa.dot.gov/query.asp?searchtype=ANY&query_type=queryCarrierSnapshot&query_param=USDOT&original_query_param=NAME'
#             payload = {'query_string': _dot}
#             headers = {'content-type': 'text/html'}
#             dot_record = requests.get(url, params=payload, headers=headers).text
#         except:
#             dot_record = 'Unable to get DOT record. '
#     msg = EmailMessage(
#         subject=email_subject, from_email=sender_email,
#         headers={'Reply-To': reply_to_email}, to=[receiver_email])
#     msg.template_name = 'pendingCompany'
#     msg.async = True
#     msg.from_name = sender_name
#     msg.metadata = {'website': 'www.traansmission.com'}
#     msg.global_merge_vars = {
#         'domain': settings.PORTAL_URL,
#         'email': _email,
#         'name': _name,
#         'phone': _phone,
#         'type': _company_type,
#         'company': _company,
#         'dot': _dot,
#         'id': _id,
#         'host': settings.HOST,
#         'dot_record': dot_record
#     }
#     msg.send()
