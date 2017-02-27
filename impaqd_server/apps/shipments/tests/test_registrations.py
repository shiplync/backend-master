import unittest
from ..models.generic_company import CompanyType
from ...notifications.models.notifications import Notification
from ...notifications.tests import validate_notification
from ...notifications.models.retention import Day1

from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
import json
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# Create your tests here.


class CarrierRegistrationClass(APITestCase):
    def test_create_carrier_owner_operator(self):
        '''Test creation of a carrier (owner operator) using the CarrierCompany
        and CarrierDriver model'''
        url = reverse('company_register')
        company = {
            "company_name": "carrier-company", "dot": 1357924, "company_type":
            CompanyType.CARRIER}
        email = "owneroperator@traansmission.com"
        user = {"email":email, "password":"owneroperatorpassword"}
        generic_user = {}
        data = {"company": company, "user": user}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify token
        token = Token.objects.get(user=User.objects.get(email=email))
        self.assertEqual(json.loads(response.content).get("token"), str(token))

        # Verify that welcome email was sent out
        notif = Notification.objects.get(
            receiver_email=user['email'],
            parent_content_type=ContentType.objects.get_for_model(Day1))
        self.assertTrue(validate_notification(notif))

class ShipperRegistrationClass(APITestCase):
    def test_create_shipper_manager(self):
        '''Test creation of a shipper using the ShipperCompany
        and ShipperManager model'''
        url = reverse('company_register')
        company = {
            "company_name": "shipper-company", "dot": 1357924, "company_type":
            CompanyType.SHIPPER}
        email = "shippersmanager@traansmission.com"
        user = {"email":email, "password":"shipperpassword"}
        data = {"company": company, "user": user}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify token
        token = Token.objects.get(user=User.objects.get(email=email))
        self.assertEqual(json.loads(response.content).get("token"), str(token))
