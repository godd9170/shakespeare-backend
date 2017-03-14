from shakespeare.settings.defaults import *

DEBUG = True

# --------------
# Allowed Hosts
# --------------
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1'
]

# ------------
# Database
# ------------

DATABASES = {
    'default' : {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'shakespearedev',
        'USER': 'shakespeareadmin',
        'PASSWORD': 'salesforce1',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}

# ------------
# Static
# ------------
STATIC_URL = '/static/'

#
#
#

ACCESS_TOKEN_EXPIRE_SECONDS = 2592000 #One Month

# ------------
# Logging
# ------------
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
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}