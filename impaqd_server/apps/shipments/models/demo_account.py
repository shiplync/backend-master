from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.auth.models import User
from django.utils import timezone

from .generic_user import GenericUser, UserType
from .generic_company import GenericCompany, CompanyType
from .company_division import (
    CompanyDivision,
    CompanyDivisionMembership,
    companydivision_post_save_create_groups,
    companydivisionmembership_post_save_set_groups)
from .relations import (
    create_company_relation, CompanyRelation, company_relation_post_save)
from .shipments import (
    Shipment, shipment_notifications)
from .locations import (
    ShipmentLocation, SavedLocation, Person, LocationType,
    AddressDetails, update_shipment_locations_order)
from .shipment_assignment import (
    ShipmentAssignment, shipmentassignment_post_save_notifications)
from .delivery_status import DeliveryStatus
from ..utils import username_from_email, reverse_geocode
from ..factories.company_division_factory import (
        CompanyDivisionFactory,
        CompanyDivisionMembershipFactory)
from faker import Faker

from impaqd_server.apps.geolocations.models import (
    Geolocation, CachedCoordinate, CachedDistance)

import os
import csv
import random
import pytz
from datetime import datetime, timedelta
from decimal import Decimal
from math import sin, cos, acos, degrees, radians


class DemoAccount(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    demo_account_type = models.CharField(
        max_length=200, choices=CompanyType.CHOICES,
        default=CompanyType.CARRIER)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100, default='flatbed')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, default='+19125552222')
    company_name = models.CharField(max_length=200)
    dot = models.IntegerField(
        unique=True, verbose_name="DOT", null=True, blank=True)

    connections = models.ManyToManyField(
        'GenericCompany', related_name='demo_account_companies', blank=True)
    company = models.ForeignKey(
        'GenericCompany', null=True, blank=True, on_delete=models.SET_NULL)

    no_of_connections = models.IntegerField(default=5)
    no_of_shipments = models.IntegerField(default=40)

    def __unicode__(self):
        return self.email


def location_from_saved_location(sl, location_type, shipment):
    address_details = AddressDetails.objects.create(
        address=sl.address_details.address, city=sl.address_details.city,
        state=sl.address_details.state, zip_code=sl.address_details.zip_code)
    contact = Person.objects.create()
    return ShipmentLocation.objects.create(
        company_name=sl.company_name, contact=contact,
        address_details=address_details, shipment=shipment,
        location_type=location_type, cached_coordinate=sl.cached_coordinate)


# def get_shipper(instance):
#     if instance.demo_account_type == CompanyType.SHIPPER:
#         return instance.company
#     else:
#         return random.choice(instance.connections.all())


def get_carrier(instance):
    if instance.demo_account_type == CompanyType.CARRIER:
        return instance.company
    else:
        return random.choice(instance.connections.all())


def create_geolocation(l1, l2, shipment):
    # Straight line between shipper and receiver
    x1 = l1.cached_coordinate.coordinate.x
    y1 = l1.cached_coordinate.coordinate.y
    x2 = l2.cached_coordinate.coordinate.x
    y2 = l2.cached_coordinate.coordinate.y
    a = (y2-y1)/(x2-x1)
    b = y2-a*x2

    # 8 points on line
    n = 8
    xs = [((float(i)+1)*((x2-x1)/float(n+1)))+x1 for i in xrange(n)]
    ys = [(a*x+b) for x in xs]

    # Random geo noise
    pm = random.choice([-1, 1])
    xs = [x+(x2-x1)*0.05*random.random()*pm for x in xs]
    pm = random.choice([-1, 1])
    ys = [y+(y2-y1)*0.05*random.random()*pm for y in ys]

    # Random dates
    picked_up_at = l1.arrival_time
    delivered_at_t = (
        l2.arrival_time if l2.arrival_time else l2.time_range.time_range_end)
    t1 = int(picked_up_at.strftime('%s'))
    t2 = int(delivered_at_t.strftime('%s'))
    ts = [int(((float(i)+1)*((t2-t1)/float(n+1)))+t1) for i in xrange(n)]
    for i in xrange(n):
        #display_text = 'Hart Expressway, Birdland County, Homeland'
        display_text = reverse_geocode(xs[i], ys[i])
        timestamp = timezone.make_aware(
            datetime.fromtimestamp(ts[i]), pytz.UTC) + \
            timedelta(milliseconds=random.randint(-10000, +10000))

        Geolocation.objects.create(
            latitude=ys[i], longitude=xs[i], timestamp=timestamp,
            carrier=shipment.carrier, driver=shipment.carrier.owner,
            display_text=display_text, shipment=shipment)

def demo_create_driver_users(no_users, instance):
    no_users = 10
    users = [0] * no_users
    for i in range(no_users):
        user = User.objects.create_user(
            username_from_email(instance.email+'test'+str(i)),
            None, instance.password)
        driver_type = UserType.CARRIER_DRIVER
        driver = GenericUser.objects.create(
            user=user, email=instance.email+'test'+str(i),
            first_name=instance.first_name+str(i),
            last_name=instance.last_name+str(i),
            phone=instance.phone, company=company,
            user_type=driver_type)
        users[i] = driver

def demo_create_division(company):
    no_divisions = 3
    target = [0] * no_divisions
    for i in range(no_divisions):
        target[i] = CompanyDivisionFactory.create(company=company)
        companydivision_post_save_create_groups(
            CompanyDivision.__class__, target[i], False, False)

def demo_create_division_membership(divisions, no_users, users):
    for i in range(no_users):
        membership = CompanyDivisionMembershipFactory(
            division=target[random.randint(0, no_divisions)], user=users[i])
        companydivisionmembership_post_save_set_groups(
            CompanyDivisionMembership, membership, False, False)

@receiver(post_save, sender=DemoAccount)
def demo_account_post_save(sender, instance, raw, created, **kwargs):
    if created:
        # Create company
        company = GenericCompany.objects.create(
            company_name=instance.company_name, verified=True,
            registration_complete=True,
            company_type=instance.demo_account_type)

        user = User.objects.create_user(
            username_from_email(instance.email),
            None, instance.password)

        manager_type = None
        if instance.demo_account_type == CompanyType.SHIPPER:
            manager_type = UserType.BROKER_MANAGER
            driver_types = [UserType.BROKER_REPRESENTATIVE,
                UserType.BROKER_SUPERVISOR]
        else:
            manager_type = UserType.CARRIER_MANAGER
            driver_types = [UserType.CARRIER_DRIVER,
                UserType.CARRIER_SUPERVISOR]

        manager = GenericUser.objects.create(
            user=user, email=instance.email,
            first_name=instance.first_name, last_name=instance.last_name,
            phone=instance.phone, company=company,
            user_type=manager_type)

        fake = Faker()
        # Drivers start
        no_users = 10
        users = [0] * no_users
        for i in range(no_users):
            email = fake.email()
            user = User.objects.create_user(
                username_from_email(email),
                None, instance.password)
            driver_type = driver_types[random.randint(0, len(driver_types)-1)]
            driver = GenericUser.objects.create(
                user=user, email=email,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone=fake.phone_number(), # perserve 10 digits
                company=company,
                user_type=driver_type)
            users[i] = driver

        # Drivers end

        # Division start
        no_divisions = 3
        target = [0] * no_divisions
        for i in range(no_divisions):
            target[i] = CompanyDivisionFactory.create(company=company)
            companydivision_post_save_create_groups(
                CompanyDivision.__class__, target[i], False, False)

        # Division end

        # Membership start
        for i in range(no_users):
            membership = CompanyDivisionMembershipFactory(
                division=target[random.randint(0, no_divisions-1)], user=users[i])
            companydivisionmembership_post_save_set_groups(
                CompanyDivisionMembership, membership, False, False)
        # Membership end

        company.owner = manager
        company.save()
        instance.company = company

        post_save.disconnect(
            receiver=company_relation_post_save,
            sender=CompanyRelation)
        for i in xrange(instance.no_of_connections):
            # Create connections
            con_company_type = None
            if instance.demo_account_type == CompanyType.SHIPPER:
                con_company_type = CompanyType.CARRIER
            else:
                con_company_type = CompanyType.SHIPPER
            con_company = GenericCompany.objects.create(
                company_name=('COMPANY %i' % (i+1)), verified=True,
                dot=random.randint(1000000, 9999999),
                company_type=con_company_type,
                registration_complete=True)
            con_email = ('demoaccount+%i-%i@traansmission.com' % (
                i+1, company.id))
            con_user = User.objects.create_user(
                username_from_email(con_email),
                None, instance.password)
            con_manager_type = None
            if instance.demo_account_type == CompanyType.SHIPPER:
                con_manager_type = UserType.CARRIER_MANAGER
            else:
                con_manager_type = UserType.BROKER_MANAGER
            con_manager = GenericUser.objects.create(
                user=con_user, email=con_email,
                first_name='Bob', last_name='D.',
                phone = '+19125552222', company=con_company,
                user_type=con_manager_type)
            con_company.owner = con_manager
            con_company.save()
            instance.connections.add(con_company)
            create_company_relation(con_company, company)
        post_save.connect(
            receiver=company_relation_post_save,
            sender=CompanyRelation)

        # Create saved locations
        try:
            file_path = os.path.join(
                settings.BASE_DIR,
                '../scripts/CompanyLocations.csv')
            with open(file_path, 'rU') as f:
                reader = csv.reader(f)
                location_tuples = [line for line in reader]

            for (name, phone, address_str, lat, lng, city, state) \
                    in location_tuples:
                address_fields = address_str.split(',')
                address = address_fields[0]
                zip_code = address_fields[len(address_fields)-1].strip()
                pt = Point(float(lat), float(lng))
                c = CachedCoordinate.objects.create(
                    address=address, coordinate=pt)
                address_details = AddressDetails.objects.create(
                    address=address, city=city, state=state, zip_code=zip_code)
                phone = '+19125552222'
                person = Person.objects.create(
                    first_name='Joe', last_name='Johnson',
                    email=instance.email, phone=phone)
                SavedLocation.objects.create(
                    company_name='%s - %s' % (name, city),
                    address_details=address_details,
                    owner=instance.company, contact=person,
                    cached_coordinate=c)
        except Exception:
            import traceback
            print traceback.format_exc()

        # Create shipments from saved locations
        post_save.disconnect(receiver=shipment_notifications, sender=Shipment)
        post_save.disconnect(
            receiver=shipmentassignment_post_save_notifications,
            sender=ShipmentAssignment)
        seed = 2017
        random.seed(seed)
        for i in xrange(instance.no_of_shipments):
            owner = instance.company
            # Number of extra locations (additional to first and last location)
            extra_location_count = random.randint(0, 2)

            # Random shipment status
            status = random.choice([c[0] for c in DeliveryStatus.CHOICES])

            # Set carrier
            carrier = None
            carrier_is_approved = False
            if status in DeliveryStatus.HAS_CARRIER_STATUSES:
                carrier = get_carrier(instance)
            if status in DeliveryStatus.CARRIER_APPROVED_STATUSES:
                carrier_is_approved = True

            s = Shipment.objects.create(
                owner=owner, owner_user=owner.owner,
                carrier=carrier, carrier_is_approved=carrier_is_approved)

            # Delete empty default locations
            s.locations.all().delete()

            # Create new pickup and dropoff
            location_from_saved_location(
                random.choice(owner.savedlocation_set.all()),
                LocationType.PICKUP, s)
            location_from_saved_location(
                random.choice(owner.savedlocation_set.all()),
                LocationType.DROPOFF, s)

            # Create extra optional locations
            for i in xrange(extra_location_count):
                location_from_saved_location(
                    random.choice(owner.savedlocation_set.all()),
                    random.choice([c for c in LocationType.VALID_TYPES]), s)

            # Set location info
            date_now = datetime.now().replace(second=0, microsecond=0)
            for l in s.locations.all():
                # Weight
                l.features.weight = (random.randint(4, 12)*400)
                l.features.save()

                # Time range
                ds = random.randint(-8000, -4000)
                l.time_range.time_range_start = date_now + timedelta(seconds=ds)
                ds = random.randint(4000, 8000)
                l.time_range.time_range_end = date_now + timedelta(seconds=ds)
                l.time_range.save()

                # Arrival time
                if (status == DeliveryStatus.ENROUTE or
                        status == DeliveryStatus.DELIVERED):
                    ds = random.randint(-8000, 8000)
                    l.arrival_time = date_now + timedelta(seconds=ds)
                    l.save()

                date_now = date_now + timedelta(days=1)

            # Set first and last location on shipment + next_location
            update_shipment_locations_order(s)

            # Set distance to next location(s)
            for l in s.locations.all():
                if l.next_location:
                    start_lat = l.cached_coordinate.latitude
                    start_lon = l.cached_coordinate.longitude
                    end_lat = l.next_location.cached_coordinate.latitude
                    end_lon = l.next_location.cached_coordinate.longitude
                    distance_meters = (
                        sin(radians(start_lat)) *
                        sin(radians(end_lat)) +
                        cos(radians(start_lat)) *
                        cos(radians(end_lat)) *
                        cos(radians(start_lon - end_lon)))
                    distance_meters = (
                        degrees(acos(distance_meters))) * 69.09 * 1609.34
                    distance = Decimal.from_float(distance_meters)
                    d = CachedDistance.objects.create(
                        start_lat=start_lat, end_lat=end_lat,
                        start_lon=start_lon, end_lon=end_lon,
                        distance=distance)
                    l.cached_distance = d
                    l.save()

            # Payout
            price_per_mile = random.uniform(2.50, 3.9)
            s.payout_info.payout = Decimal(
                int(float(s.trip_distance) * price_per_mile * 0.000621371))

            s.payout_info.save()
            # Assign to carrier(s)
            assignee = s.carrier if s.carrier else get_carrier(instance)
            ShipmentAssignment.objects.create(
                shipment=s, assignee=assignee, assigner=s.owner.owner,
                parent=s.owner, r=True)

            # Create geolocations
            if (status == DeliveryStatus.ENROUTE or
                    status == DeliveryStatus.DELIVERED):
                for l in s.locations.all():
                    if l.next_location:
                        create_geolocation(l, l.next_location, s)

            s.save()
        instance.save()
        post_save.connect(receiver=shipment_notifications, sender=Shipment)
        post_save.connect(
            receiver=shipmentassignment_post_save_notifications,
            sender=ShipmentAssignment)

        instance.save()
        post_save.connect(receiver=shipment_notifications, sender=Shipment)
        post_save.connect(
            receiver=shipmentassignment_post_save_notifications,
            sender=ShipmentAssignment)


@receiver(pre_delete, sender=DemoAccount)
def demo_account_pre_delete(sender, instance, **kwargs):
    # Delete all companies
    if instance.company:
        company_id = instance.company.id
        instance.company.delete()
        for i in xrange(instance.no_of_connections):
            con_email = ('demoaccount+%i-%i@traansmission.com' % (
                i+1, company_id))
            res = GenericUser.objects.filter(email=con_email)
            if res.count():
                res[0].company.delete()
