from ..models.generic_company import GenericCompany, CompanyType
from ..serializers.carriers import CarrierVerificationSerializer
from impaqd_server.apps.shipments import notifications

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authentication import (
    TokenAuthentication, BasicAuthentication)
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics


@api_view(['GET'])
def verify_company(request, pk, send_email):
    company = GenericCompany.objects.get(pk=pk)
    if company.rejected:
        return Response('This company has already been rejected')
    if not company.verified:
        company.verified = True
        company.save()
        if int(send_email):
            if company.company_type == CompanyType.SHIPPER:
                notifications.shippers.signup_approved(company)
            elif company.company_type == CompanyType.CARRIER:
                notifications.carriers.signup_approved(company)
        return Response('You have successfully verified this company')
    else:
        return Response('This company has already been verified')


@api_view(['GET'])
def reject_company(request, pk, send_email):
    company = GenericCompany.objects.get(pk=pk)
    was_rejected = company.rejected
    if company.verified:
        return Response('This company has already been verified')
    if not was_rejected:
        company.rejected = True
        company.save()
        if int(send_email):
            if company.company_type == CompanyType.SHIPPER:
                notifications.shippers.signup_declined(company)
            elif company.company_type == CompanyType.CARRIER:
                notifications.carriers.signup_declined(company)
        return Response('You have successfully rejected this company')
    else:
        return Response('This company has already been rejected')


class CarrierVerificationView(generics.RetrieveAPIView):
    '''
    View that only returns carrier ID and verification status.
    '''
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = CarrierVerificationSerializer

    def get_object(self):
        return self.request.user.genericuser.company
