import csv
from django.contrib.gis.geos import Point
from django.utils import timezone
from decimal import Decimal
from datetime import datetime, timedelta, date
from copy import copy
from pytz import timezone

from django.conf import settings

est = timezone('US/Eastern')

from impaqd_server.apps.shipments.models import Shipment, Location

with open('scripts/Shipments.csv', 'rU') as f:
	reader = csv.reader(f)
	shipment_tuples = [line for line in reader]

with open('scripts/CompanyLocations2.csv', 'rU') as f:
	reader = csv.reader(f)
	location_tuples = [line for line in reader]

location_map = {}
for (name, phone, address, lat, lng, city, state) in location_tuples:
	address = address.replace(', United States of America', '')
	address_fields = address.split(',')
	address1 = address_fields[0]
	address2 = ','.join(address_fields[1:])
	address = "%s\n%s" % (address1.strip(), address2.strip())

	key = "%s (%s, %s)" % (name.upper(), city.upper(), state.upper())
	name = ' '.join([word.capitalize() for word in name.split()])
	pt = Point(float(lat), float(lng))
	
	location_map[key] = Location.objects.create(
		name=name,
		phone=phone,
		address=address,
		coordinate=pt)

shipment_dicts = []
for line in shipment_tuples:
	(sid, vehicle, payout, carrier, 
	 shipper_key, dpickup_start, tpickup_start, 
	 dpickup_end, tpickup_end, pickup_dock, dpickedup, tpickedup,
	 receiver_key, ddelivery_start, tdelivery_start, 
	 ddelivery_end, tdelivery_end, delivery_dock, ddelivery, tdelivery) = line
	location = location_map[shipper_key]

	if (vehicle.upper() == 'FLATBED'):
		vehicle_type = 1
	elif (vehicle.upper() == 'REEFER'):
		vehicle_type = 2
	elif (vehicle.upper() == 'VAN'):
		vehicle_type = 3
	else:
		raise Exception(vehicle)

	tpickup_start = '%04d' % int(tpickup_start)
	tdelivery_start = '%04d' % int(tdelivery_start)
	delta_delivery_pickup = datetime.strptime(ddelivery_start+tdelivery_start, '%Y%m%d%H%M') - datetime.strptime(dpickup_start+tpickup_start, '%Y%m%d%H%M')
	
	pick_up_time_range_start = datetime.strptime(dpickup_start+tpickup_start, '%Y%m%d%H%M')

	d = dict(
		shipment_id=sid,
		vehicle_type=vehicle_type,
		payout=Decimal(payout),
		shipper=location_map[shipper_key],
		pick_up_time_range_start=pick_up_time_range_start,
		pick_up_dock=pickup_dock,
		receiver=location_map[receiver_key],
		delivery_dock=delivery_dock,
		delta_delivery_pickup=delta_delivery_pickup
	)
	shipment_dicts.append(d)

iters = 0
num_in_day = 1
target_date = date.today()
#end_date = date(2014, 6, 1)
end_date = date(2014, 10, 1)
total_rows = len(shipment_dicts)

print 'starting to save shipments'
while target_date < end_date:
	target_date_str = target_date.strftime('%Y%m%d')
	d = copy(shipment_dicts[iters % total_rows])

	tpickup_start = d['pick_up_time_range_start'].strftime('%H%M')
	pick_up_time_range_start = datetime.strptime(target_date_str+tpickup_start, '%Y%m%d%H%M').replace(tzinfo=est)
	
	cycle = (iters // total_rows) + 1
	if cycle > 1:
		d['shipment_id'] = d['shipment_id'] + ('-%d' % cycle)
	
	delta_delivery_pickup = d.pop('delta_delivery_pickup')
	delivery_time_range_start = pick_up_time_range_start + delta_delivery_pickup

	d['pick_up_time_range_start'] = pick_up_time_range_start
	d['pick_up_time_range_end'] = pick_up_time_range_start+timedelta(hours=2)
	d['delivery_time_range_start'] = delivery_time_range_start
	d['delivery_time_range_end'] = delivery_time_range_start+timedelta(hours=2)
	print 'saving shipment'
	s = Shipment.objects.create(**d)

	iters += 1
	num_in_day += 1
	if num_in_day >= 20:
		target_date = target_date + timedelta(days=1)
		num_in_day = 0
