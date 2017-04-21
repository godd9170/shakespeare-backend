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


# ------------
# CORS Settings
# ------------
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = (
'x-requested-with',
'content-type',
'accept',
'origin',
'authorization',
'X-CSRFToken'
)
#CORS_ORIGIN_WHITELIST = ('null') #chrome-extensions use null


# -------------
# Oauth 
# -------------
OAUTH_APPLICATION_NAME = "django-app-test"
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

# MIDDLEWARE.append('rollbar.contrib.django.middleware.RollbarNotifierMiddleware')
# ROLLBAR = {
#     'access_token': '38b1269535074f1a9b4c7da6a8142502',
#     'environment': 'local',
#     'root': BASE_DIR,
# }
# import rollbar
# rollbar.init(**ROLLBAR)

# -------------
# Celery
# -------------
PERFORM_ASYNCHRONOUS = True #True #Run the asyncronous tasks (i.e. research fetching)