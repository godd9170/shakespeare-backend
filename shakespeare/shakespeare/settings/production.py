from shakespeare.settings.defaults import *

DEBUG = True #Just for now

# --------------
# Allowed Hosts
# --------------
ALLOWED_HOSTS = [
    'production.sfpvwpungj.us-east-1.elasticbeanstalk.com',
    'default-environment.hjt2m2vmx2.us-east-1.elasticbeanstalk.com'
]


# ------------
# Database
# ------------
DATABASES = {
    'default' : {
        'ENGINE' : 'django.db.backends.postgresql_psycopg2',
        'NAME' : os.environ['RDS_DB_NAME'],
        'USER' : os.environ['RDS_USERNAME'],
        'PASSWORD' : os.environ['RDS_PASSWORD'],
        'HOST' : os.environ['RDS_HOSTNAME'],
        'PORT' : os.environ['RDS_PORT'],
    }
}

# ------------
# Static
# ------------
STATIC_ROOT = os.path.join(BASE_DIR, "..", "www", "static")
STATIC_URL = '/static/'

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
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/var/log/app_logs/django_debug.log',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}