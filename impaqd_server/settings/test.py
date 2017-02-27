# Test-specific settings file. Inherits all settings in common.py.
#
# The tests environment requires the following keys to be set in
# secrets.py:
#
# - SECRET_KEY
# - DATABASE_URL

import os
from impaqd_server.settings.common import *

DEBUG = True
TEMPLATE_DEBUG = True

import dj_database_url
DATABASES = {'default': dj_database_url.parse(DATABASE_URL)}
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'

EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
#EMAIL_FILE_PATH = '/tmp/email-testing' # change this to a proper location

LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
            },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'file.log',
            'formatter': 'simple'
            },
        },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'DEBUG'
        },
        'django.db.backends': {
            'handlers': ['null'],  # Quiet by default!
            'propagate': False,
            'level': 'INFO'
        },
        'impaqd': {
            'handlers': ['stderr', 'console'],
            'level': 'WARNING',
            'propagate': True
        }
    }
}

if DEBUG:
    # make all loggers use the console.
    for logger in LOGGING['loggers']:
        LOGGING['loggers'][logger]['handlers'] = ['console']

INSTALLED_APPS += (
    'debug_toolbar',
    'test_without_migrations',
    )

TEST_RUNNER = 'xmlrunner.extra.djangotestrunner.XMLTestRunner'
TEST_OUTPUT_DIR = 'unittest'
if hasattr(os.environ, 'CIRCLE_TEST_REPORTS'):
    TEST_OUTPUT_DIR = os.path.join(os.environ['CIRCLE_TEST_REPORTS'], 'unittest')

CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
