import httplib
import json
from django.http import HttpResponse
import os
import boto
from boto.s3.key import Key
from django.conf import settings
import PIL
from PIL import Image
import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import requests
import re
from math import sin, cos, acos, degrees, radians
from decimal import Decimal


def json_response(response_dict, status=200):
    response = HttpResponse(json.dumps(response_dict), content_type="application/json", status=status)
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


def test_network_connectivity():
    conn = httplib.HTTPConnection("api.traansmission.com")
    try:
        conn.request("HEAD", "/")
        return True
    except:
        return False


def username_from_email(email):
    """
    Due to the limitation of that username fields on
    the user model can't be longer than 30 chars, we use
    this function to trim the username when saving/updating 
    username field. the username and email field are always
    the same, except when email is more than 30 chars long. 
    """
    return (email[:30]) if len(email) > 30 else email

def get_1_pixel_photo_base64():
    return "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNgYAAAAAMAASsJTYQAAAAASUVORK5CYII="

def create_or_update_remote_file(file_context, file_obj):
    calling_format = 'boto.s3.connection.OrdinaryCallingFormat'
    conn = boto.connect_s3(calling_format=calling_format)
    bucket_name = (settings.S3_BUCKET_PREFIX + '-' + file_context.path).replace('_','-')
    bucket = conn.create_bucket(bucket_name)
    k = Key(bucket, file_context.uuid_value)
    k.set_contents_from_file(file_obj)
    file_context.save()


def delete_remote_file(file_context):
    calling_format = 'boto.s3.connection.OrdinaryCallingFormat'
    conn = boto.connect_s3(calling_format=calling_format)
    bucket_name = (settings.S3_BUCKET_PREFIX + '-' + file_context.path).replace('_','-')
    try:
        bucket = conn.get_bucket(bucket_name)
        bucket.delete_key(file_context.uuid_value)
    except Exception, e:
        pass


def get_expiring_file_url(file_context):
    has_internet = test_network_connectivity()
    if has_internet:
        try:
            # When using dot notation in bucket names, we MUST use following
            # calling format when generating a url.
            calling_format = 'boto.s3.connection.OrdinaryCallingFormat'
            conn = boto.connect_s3(calling_format=calling_format)
            bucket_name = (settings.S3_BUCKET_PREFIX + '-' +
                    file_context.path).replace('_', '-')
            k = Key(conn.get_bucket(bucket_name), file_context.uuid_value)
            return k.generate_url(expires_in=file_context.url_ttl)
        except Exception, e:
            print 'Unable to get expiring file url from S3'
            print str(e)
            return ''
    else:
        return None

def update_user(instance):
    user = instance.user
    if user:
        user.email = instance.email
        # Trim username if it's more than 30 chars long. 
        user.username = username_from_email(instance.email)
        user.save()     

def resize_image(image, size):
    """Resizes an image according to the size argument

    image -- file pointer to an Django File object (jpg or png is tested)
    size -- comma separated width, height value. e.g. `100, 100`

    returns -- file pointer to resized image

    references:
    http://stackoverflow.com/a/4544525/2457624
    """
    im = Image.open(image).convert('RGB') 
    im.thumbnail(size, Image.ANTIALIAS)
    im_io = StringIO.StringIO()
    im.save(im_io, format='JPEG')
    resized_im = InMemoryUploadedFile(im_io, None, 'temp.jpg',
    'image/jpeg', im_io.len, None)
    return resized_im

def get_trip_dist(start_lon, start_lat, end_lon, end_lat):
    """Calculate trip distance from pickup and delivery location

    When testing, dont calculate using a geocoding webservice.
    If Geocoding fails, fall back to using Euclidean distance
    """
    if not settings.TESTING:
        try:
            origin = str(start_lat) + ',' + str(start_lon)
            dest = str(end_lat) + ',' + str(end_lon)
            base_url = 'http://maps.googleapis.com/maps/api/distancematrix/json'
            headers = {'content-type': 'application/json'}
            data = {'origins': origin, 'destinations': dest, 'units': 'imperial'}
            response = requests.get(base_url, params=data, headers=headers)
            distance_meters = int(
                response.json()['rows'][0]['elements'][0]['distance']['value'])
            if distance_meters > 10:
                print 'using google trip dist'
                return distance_meters
        except:
            pass
    distance_meters = (sin(radians(start_lat)) *
                    sin(radians(end_lat)) +
                    cos(radians(start_lat)) *
                    cos(radians(end_lat)) *
                    cos(radians(start_lon - end_lon)))
    distance_meters = (degrees(acos(distance_meters))) * 69.09 * 1609.34
    print 'using naive trip dist'
    return Decimal.from_float(distance_meters)


def truncate_string(str, len=15, use_dots=True):
    """Truncate a  string with or without `..` appended"""
    post_fix = '..' if use_dots else ''
    return str[:len] + (str[len:] and post_fix)


def reverse_geocode(lon, lat):
    if not settings.TESTING:
        try:
            base_url = 'http://nominatim.openstreetmap.org/reverse'
            headers = {'content-type': 'application/json'}
            data = {'format': 'json', 'lat': lat, 'lon': lon}
            response = requests.get(base_url, params=data, headers=headers)
            display_name = response.json()['display_name']
            if display_name and len(display_name) > 0:
                display_name = display_name.replace(
                    ', United States of America', '')
                return display_name
            else:
                print 'unable to geocode lat and lon'
                return 0
        except:
            print 'unable to geocode lat and lon'
            return 0
