from impaqd_server.apps.shipments.utils import username_from_email
from ..models.generic_company import CompanyType
from ..utils import json_response
from ..serializers.carriers import CarrierVerificationSerializer

from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes)
from rest_framework.authentication import (
    TokenAuthentication, BasicAuthentication)
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import generics

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse


@csrf_exempt
@api_view(['POST'])
# This login is generic
def login(request):
    if request.method == 'POST':
        username = request.data['username']
        # Make username case insensitive
        username = username.lower()
        # Trim username if it's more than 30 chars long.
        username_trimmed = username_from_email(username)
        password = request.data['password']

        if username is not None and password is not None:
            user = authenticate(username=username_trimmed, password=password)
            if (user is not None and user.is_active and
                    hasattr(user, 'genericuser')):
                    return json_response({
                        'token': str(Token.objects.get_or_create(
                            user=user)[0]),
                        'email': user.genericuser.email,
                        'usertype': user.genericuser.user_type,
                    })
            else:
                return json_response({
                    'error': 'Invalid Username/Password'
                }, status=401)
        else:
            return json_response({
                'error': 'Invalid Data'
            }, status=400)
    elif request.method == 'OPTIONS':
        return json_response({})
    else:
        return json_response({
            'error': 'Invalid Method'
        }, status=405)


@csrf_exempt
@api_view(['POST'])
# This logout is generic
def logout(request):
    if request.method == 'POST':
        return json_response({
            'status': 'success'
        })
    elif request.method == 'OPTIONS':
        return json_response({})
    else:
        return json_response({
            'error': 'Invalid Method'
        }, status=405)


@csrf_exempt
@api_view(['GET'])
@authentication_classes((TokenAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def verify_token(request):
    return json_response({
        'token_ok': True
        })


@csrf_exempt
@api_view(['POST'])
@authentication_classes((TokenAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def change_password(request):
    if request.method == 'POST':
        new_password = request.data.get('new_password')
        old_password = request.data.get('old_password')
        if new_password and old_password:
            user = request.user
            print user.check_password(old_password)
            if user.check_password(old_password):
                try:
                    user.set_password(new_password)
                    user.save()
                    return json_response({
                        'success': True
                    })
                except Exception, e:
                    print str(e)
                    return json_response(
                        'Unable to set new password',
                    status=400)  
            else:
                return json_response(
                    'Old password was incorrect',
                status=400)
        else:
            return json_response(
                    'You must supply a new and an old password',
                status=400)          
    elif request.method == 'OPTIONS':
        return json_response({})
    else:
        return json_response({
            'Invalid Method'
        }, status=405)     


@csrf_exempt
@api_view(['POST'])
def reset_password(request):
    if request.method == 'POST':
        is_admin_site=False
        template_name='passwords/password_reset_form.html'
        email_template_name='passwords/password_reset_email.html'
        subject_template_name='passwords/password_reset_subject.txt'
        password_reset_form=PasswordResetForm
        token_generator=default_token_generator
        post_reset_redirect=None
        from_email=None
        current_app=None
        extra_context=None
        html_email_template_name='passwords/password_reset_email_html.html'
        if post_reset_redirect is None:
            post_reset_redirect = reverse('password_reset_done')
        else:
            post_reset_redirect = resolve_url(post_reset_redirect)
        if request.method == "POST":
            form = password_reset_form(request.data)
            if form.is_valid():
                opts = {
                    'use_https': request.is_secure(),
                    'token_generator': token_generator,
                    'from_email': from_email,
                    'email_template_name': email_template_name,
                    'subject_template_name': subject_template_name,
                    'request': request,
                    #'html_email_template_name': html_email_template_name, #Only works for Django 1.7
                }
                form = PasswordResetForm(request.data)
                form.is_valid()
                form.save(**opts)       
                return json_response({
                    'success': True
                }, status=200)
        else:
            return json_response({
                'error': 'Invalid Method'
            }, status=405)        
