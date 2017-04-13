import os
from .defaults import *

DEBUG = True #Just for now

# --------------
# Allowed Hosts
# --------------
ALLOWED_HOSTS = [
    'shakespeare-development.us-east-1.elasticbeanstalk.com',
    'dev.shakespeare.ai',
    'localhost'
]


# ------------
# Database
# ------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['RDS_DB_NAME'],
        'USER': os.environ['RDS_USERNAME'],
        'PASSWORD': os.environ['RDS_PASSWORD'],
        'HOST': os.environ['RDS_HOSTNAME'],
        'PORT': os.environ['RDS_PORT'],
    }
}

# ------------
# Static
# ------------
STATIC_ROOT = os.path.join(BASE_DIR, "..", "www", "static")
STATIC_URL = '/static/'

# ------------
# CORS Settings
# ------------
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True #We'll leave this true for now, but should be toggled of in the future
# CORS_ORIGIN_WHITELIST = (
#     'google.com',
#     'hostname.example.com',
#     'localhost:8000',
#     '127.0.0.1:9000'
# )

# -------------
# Oauth 
# -------------
OAUTH_APPLICATION_NAME = "shakespeare-dev"
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

MIDDLEWARE.append('rollbar.contrib.django.middleware.RollbarNotifierMiddleware')
ROLLBAR = {
    'access_token': '38b1269535074f1a9b4c7da6a8142502',
    'environment': 'development',
    'root': BASE_DIR,
}
import rollbar
rollbar.init(**ROLLBAR)

# -------------
# Celery
# -------------
PERFORM_ASYNCHRONOUS = True #Run the asyncronous tasks (i.e. research fetching)

# REDIS related settings
REDIS_HOST = 'redis-dev.u7sr1d.ng.0001.use1.cache.amazonaws.com'
REDIS_PORT = '6379'

# CELERY related settings
BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'