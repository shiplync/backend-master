import base64
import json
import os
import random

from optparse import make_option

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
User = get_user_model()

from impaqd_server.apps.shipments.models import Shipment, Carrier, Shipper, GlobalSettings
from impaqd_server.apps.shipments.factories import UserFactory, ShipperFactory, CarrierFactory, LocationFactory, ShipmentFactory

from pprint import pprint


class Command(BaseCommand):
      help = 'seed the database'

      option_list = BaseCommand.option_list + (
            make_option('--no-flush',
                        action='store_false',
                        dest='flush',
                        default=True,
                        help='Do not flush the database before creating seeds'),
            make_option('--fixture',
                        action='store', type='string',
                        dest='fixture',
                        default=None,
                        help='Fixture file to use create seeds')
      )
      
      def handle(self, *args, **options):
            if options['flush']:
                  call_command('flush', interactive=False)

            if options['fixture']:
                  fixture_path = os.path.join(settings.BASE_DIR, options['fixture'])
                  with open(fixture_path) as file:
                            fixture_data = json.load(file)

            GlobalSettings.objects.create(shipment_id_counter=random.randrange(100));
            shipper = self._create_shipper(fixture_data['shipper'])
            print("Created Shipper (%s)" % (shipper.email))

            carrier = self._create_carrier(fixture_data['carrier'])
            print("Created Carrier (%s)" % (carrier.email))
            
      def _create_user(self, user_data):
            return UserFactory.create(**user_data)

      def _create_shipper(self, shipper_data):
            if 'user' in shipper_data:
                  user = self._create_user(shipper_data['user'])
                  shipper_data['user'] = user
            
            return ShipperFactory.create(**shipper_data)

      def _create_carrier(self, carrier_data):
            if 'user' in carrier_data:
                  user = self._create_user(carrier_data['user'])
                  carrier_data['user'] = user

            if 'photo_file' in carrier_data:
                  photo_path = os.path.join(settings.BASE_DIR, carrier_data['photo_file'])
                  with open(photo_path, 'rb') as photo_file:
                        photo = base64.b64encode(photo_file.read())
                        del carrier_data['photo_file']
                        carrier_data['photo'] = photo

            return CarrierFactory.create(**carrier_data)
