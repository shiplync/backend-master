from ..models.generic_user import GenericUser, UserType
from ..models.generic_company import GenericCompany, CompanyType
from ..utils import json_response, username_from_email
from ..tasks import task_new_company_handle_verification
from ..serializers.generics import GenericCompanySerializer
from ...payments.serializers import SubscriptionSerializer

from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import (
    TokenAuthentication, BasicAuthentication)

from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.db import transaction
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from phonenumber_field.modelfields import validate_international_phonenumber

import logging
LOG = logging.getLogger('impaqd')


@csrf_exempt
@api_view(['POST'])
def register_carrier(request):
    return register_company_and_user(request, CompanyType.CARRIER)


@csrf_exempt
@api_view(['POST'])
def register_shipper(request):
    return register_company_and_user(request, CompanyType.SHIPPER)


@csrf_exempt
@api_view(['POST'])
# def register_company_and_user(request, company_type):
def register_company_and_user(request):
    company_type = request.data['company']['company_type']
    user_type = None
    company_slug = None
    if company_type == CompanyType.SHIPPER:
        user_type = UserType.BROKER_MANAGER
    elif company_type == CompanyType.CARRIER:
        user_type = UserType.CARRIER_MANAGER

    if request.method == 'POST':
        # Verify that user information was provided
        # Try to get email from request. If it is not there, set email to None
        email = (
            request.data['user']['email']
            if ('user' in request.data and 'email' in request.data['user'])
            else None)

        # Try to get password from request. If it is not there,
        # set password to None
        password = (
            request.data['user']['password']
            if ('user' in request.data and 'password' in request.data['user'])
            else None)
        if not (email and password):
            return json_response({
                'error': 'You must supply a user with an email and password'
            }, status=406)

        # Check that a user with this email does not exist
        response = check_if_user_exists_with_responses(email)
        if response:
            return response
        # Create a company with posted data
        company = None
        try:
            data = request.data['company']
            # data['company_type'] = company_type
            company = GenericCompany.objects.create(**data)
        except TypeError, e:
            return json_response({
                'error': (
                    'You must supply the right parameters '
                    'to the company object.'),
                'detail': str(e)
            }, status=406)
        except IntegrityError, e:
            return json_response({
                'error': 'Company already exists.',
                'detail': str(e)
            }, status=409)

        # Create user
        user = None
        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username_from_email(email), None, password)
        except Exception, e:
            # Delete previously created objects
            company.delete()
            return json_response({
                'error': (
                    'Unable to create user with that username and password.'),
                'detail': str(e)
            }, status=406)

        # Create generic user
        generic_user = None
        try:
            args = {'user': user, 'email': email, 'company': company,
                    'user_type': user_type}
            # If generic_user object exists, add that data as well
            user_data = (
                request.data['generic_user']
                if ('generic_user' in request.data) else None)
            if user_data:
                if user_data['phone']:
                    validate_international_phonenumber(user_data['phone'])
                args.update(**user_data)
            with transaction.atomic():
                generic_user = GenericUser.objects.create(**args)
                company.owner = generic_user
                company.save()
        except Exception, e:
            # Delete previously created objects
            company.delete()
            user.delete()
            err = 'Unable to create user'
            if type(e) == ValidationError and len(e.messages) > 0:
                err = '. '.join(str(x) for x in e)
            # Return string from validation error, if it exists
            return json_response({
                'error': err,
                'detail': str(e)
            }, status=406)
        # Handle verification
        task_new_company_handle_verification.delay(company)
        return json_response({
            'token': str(Token.objects.get_or_create(user=user)[0]),
            'type': company_slug
        }, status=201)
    elif request.method == 'OPTIONS':
        return json_response({})
    else:
        return json_response({
            'error': 'Invalid Method'
        }, status=405)


def check_if_user_exists_with_responses(email):
    '''Checks if a user (carrier or shipper) exists
    and throws a 409 response if so. Otherwise returns False.
    '''
    # Check if a genericuser exists
    if GenericUser.objects.filter(email=email).count():
        return json_response({
            'error': 'A user with this email already exists'
        }, status=409)
    # Check if a user exists
    elif User.objects.filter(username=username_from_email(email)).count():
        return json_response({
            'error': 'A user with this email already exists'
        }, status=409)
    else:
        return False


class RegisterCompaniesSelfView(RetrieveUpdateAPIView):
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = GenericCompanySerializer

    def get_object(self):
        return self.request.user.genericuser.company


class RegisterSubscriptionSelfView(RetrieveUpdateAPIView):
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = SubscriptionSerializer

    def get_object(self):
        return self.request.user.genericuser.company.subscription
