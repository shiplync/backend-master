"""
Django settings for impaqd_server project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
from __future__ import absolute_import
# ^^^ The above is required if you want to import from the celery
# library.  If you don't have this then `from celery.schedules import`
# becomes `proj.celery.schedules` in Python 2.x since it allows
# for relative imports by default.

#from .secrets import SECRETS, postgis_version

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = os.environ.get('SECRET_KEY', '12345678')
NOTIFICATION_EMAIL = os.environ.get('NOTIFICATION_EMAIL')
HOST = os.environ.get('HOST')
CERTIFICATE = os.environ.get('CERTIFICATE')

DATABASE_URL = ''
try:
    # If database username, password, host and dbname is set, use those
    postgres_host_env_name = os.environ['POSTGRES_HOST_ENV_NAME']
    postgres_host = os.environ[postgres_host_env_name]
    postgres_db = os.environ['POSTGRES_DB']
    postgres_user = os.environ['POSTGRES_USER']
    postgres_password = os.environ['POSTGRES_PASSWORD']
    DATABASE_URL = 'postgis://%s:%s@%s/%s' % (
        postgres_user, postgres_password, postgres_host, postgres_db)
except Exception:
    # Default to DATABASE_URL fake path. 
    # Necessary if running collectstatic without a database
    DATABASE_URL = os.environ.get('DATABASE_URL', 'postgis://:@/')

PORTAL_URL = os.environ.get('PORTAL_URL')
DEBUG = (os.getenv('DEBUG', '') == 'true')
TEMPLATE_DEBUG = False
S3_BUCKET_PREFIX = os.environ.get('S3_BUCKET_PREFIX')
# these are optional for now and will be set to NONE if not defined
TEST_DATABASE_URL = os.environ.get('TEST_DATABASE_URL')
TEST_CARRIER_EMAIL = os.environ.get('TEST_CARRIER_EMAIL')
TEST_SHIPPER_EMAIL = os.environ.get('TEST_SHIPPER_EMAIL')
TOS_CURRENT_VERSION = os.environ.get('TOS_CURRENT_VERSION')

# Detect if testing
TESTING = False
try:
    TESTING = sys.argv[1:2] == ['test']
except Exception, e:
    pass
if TESTING:
    CELERY_ALWAYS_EAGER = True
    CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

'''POSTGIS_VERSION evn var must be in the following format:
'2 1' for postgis version 2.1
or
'2 1 2' for postgis version 2.1.2
'''
POSTGIS_VERSION = tuple(map(int,os.environ.get('POSTGIS_VERSION', '2 1').split(' ')))

# define in deployment-specific file
ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    # pre-installed Django packages
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',

    # third-party packages
    #'south',
    'rest_framework',
    'django_filters',
    'crispy_forms',
    'rest_framework.authtoken',
    #'djrill',
    'import_export',
    'solo',
    'django_extensions',
    'guardian',
    #'django_ses',

    # our apps
    'impaqd_server.apps.shipments',
    'impaqd_server.apps.geolocations',
    'impaqd_server.apps.permissions',
    'impaqd_server.apps.notifications',
    'impaqd_server.apps.payments',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'impaqd_server.middleware.crossdomainxhr.XsSharing',
)

ROOT_URLCONF = 'impaqd_server.urls'

WSGI_APPLICATION = 'impaqd_server.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# define in deployment-specific file
DATABASES = {
    'default': {
    }
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # this is default
    'guardian.backends.ObjectPermissionBackend',
)
ANONYMOUS_USER_ID = -1

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Eastern'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

# Django templates
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates/'),
)

CRISPY_TEMPLATE_PACK = 'bootstrap3'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}

#MANDRILL_API_KEY = "4qd-DWdhRL0p6EWJpBEg8w"
#EMAIL_BACKEND = "django_ses.SESBackend"
SENDGRID_API_KEY = "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"
EMAIL_BACKEND = "sgbackend.SendGridBackend"
DEFAULT_FROM_EMAIL = 'support@traansmission.com'

# Celery and Rabbit MQ
# Set BROKER_URL from either BROKER_HOST_ENV_NAME or CELERY_BROKER_URL
BROKER_URL = ''
try:
    broker_host_env_name = os.environ['BROKER_HOST_ENV_NAME']
    broker_host = os.environ[broker_host_env_name]
    BROKER_URL = 'amqp://guest:@%s:5672//' % broker_host
except Exception:
    BROKER_URL = os.environ.get('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = 'amqp'
CELERY_TASK_RESULT_EXPIRES = 18000  # 5 hours.
from .periodic import *
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
