# Production-specific settings file. Inherits all settings in common.py.
# 
# The production environment requires the following keys to be set in 
# secrets.py:
# 
# - SECRET_KEY
# - DATABASE_URL
#
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/ before
# deployment.

import sys
from impaqd_server.settings.common import *

TEMPLATE_DEBUG = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'www', 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
#MEDIA FILE (user uploaded files)
MEDIA_ROOT = os.path.join(BASE_DIR, 'www', 'media')
MEDIA_URL = '/media/'

# explicitly set host name of server here
# Use * for now. Change to a real host later. 
ALLOWED_HOSTS = ['*']

import dj_database_url
DATABASES = {'default': dj_database_url.parse(DATABASE_URL)}

# Prior to elastic beanstalk when only using ec2
# STATIC_ROOT = '/impaqd_static/'
# MEDIA_ROOT = '/impaqd_media/'

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
        'stderr': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'stream': sys.stderr,
            'formatter': 'simple'
        },
        'console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['stderr', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'impaqd': {
            'handlers': ['stderr', 'console'],
            'level': 'WARNING',
            'propagate': True,
        },
    }
}


# disable browsable UI in production
_DEFAULT_RENDERER_CLASSES = (
    'rest_framework.renderers.JSONRenderer',
)
try:
	REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = _DEFAULT_RENDERER_CLASSES
except NameError: 
	REST_FRAMEWORK = {
		'DEFAULT_RENDERER_CLASSES': _DEFAULT_RENDERER_CLASSES
	}
