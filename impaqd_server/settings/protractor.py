# Angular protractor backend settings file. Inherits all settings in common.py.
#
# The tests environment requires the following keys to be set in
# secrets.py:
#
# - SECRET_KEY
# - DATABASE_URL

from impaqd_server.settings.common import *

DEBUG = True
TEMPLATE_DEBUG = True

import dj_database_url
DATABASES = {'default': dj_database_url.parse(TEST_DATABASE_URL)}
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'

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
            'level': 'DEBUG',
            'propagate': True,
            },
        }
    }

if DEBUG:
    # make all loggers use the console.
    for logger in LOGGING['loggers']:
        LOGGING['loggers'][logger]['handlers'] = ['console']

INSTALLED_APPS += (
    'debug_toolbar',
    )
