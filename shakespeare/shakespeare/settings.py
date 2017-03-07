"""
Django settings for shakespeare project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'c$f9v76$n!@h=r2bfa&n2um*#8ibxe66q4nryb6o@l)_ilq(u&'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

if 'RDS_DB_NAME' in os.environ:
    DEBUG_HANDLERS = ['file']
    DEBUG_LOG_DIR = '/var/log/app_logs/django_debug.log'
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
else:
    DEBUG_HANDLERS = ['console']
    DEBUG_LOG_DIR = BASE_DIR + '/shakespeare/.logs/django_debug.log'
    DATABASES = {
        'default' : {
            'ENGINE' : 'django.db.backends.postgresql_psycopg2',
            'NAME' : 'shakespeare-dev',
            'USER' : 'shakespeareadmin',
            'PASS' : 'salesforce1',
            'HOST' : '127.0.0.1',
            'PORT' : '5432'
        }
    }

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
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
            'filename': DEBUG_LOG_DIR,
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': DEBUG_HANDLERS,
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

ALLOWED_HOSTS = [
    'default-environment.hjt2m2vmx2.us-east-1.elasticbeanstalk.com',
    'localhost',
    '127.0.0.1',
    '172.31.4.100'
]

# Google Oauth
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '17899710816-u7u7qscddvv0and0m2siteomikh7hl6e.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'yDJwJL-i3S6Yr4uiB2GXsbIi'

# Django Organizations https://github.com/bennylope/django-organizations
#ORGS_INVITATION_BACKEND = 'shakespeare.backends.MyInvitationBackend'
#ORGS_REGISTRATION_BACKEND = 'shakespeare.backends.MyRegistrationBackend'
#ORGS_SLUGFIELD = 'autoslug.fields.AutoSlugField'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'oauth2_provider',
    'social_django',
    'rest_framework_social_oauth2',
    'organizations',
    'personas.apps.PersonasConfig',
    'administration.apps.AdministrationConfig',
    'research.apps.ResearchConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'shakespeare.urls'

TEMPLATES = [
    {
        'BACKEND': 'django_jinja.backend.Jinja2',
        'APP_DIRS': False,
        'DIRS': [
            os.path.join(BASE_DIR, 'administration', 'templates')
        ],
        'OPTIONS': {
            'match_extension': '.html',
            'match_regex': r'^(?!admin/).*',
            'filters': {
                'backend_name': 'administration.filters.backend_name',
                'backend_class': 'administration.filters.backend_class',
                'icon_name': 'administration.filters.icon_name',
                'social_backends': 'administration.filters.social_backends',
                'legacy_backends': 'administration.filters.legacy_backends',
                'oauth_backends': 'administration.filters.oauth_backends',
                'filter_backends': 'administration.filters.filter_backends',
                'slice_by': 'administration.filters.slice_by'
            },
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        }
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
# Social Auth
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/done/'
SOCIAL_AUTH_STRATEGY = 'social_django.strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE = 'social_django.models.DjangoStorage'
# SOCIAL_AUTH_STORAGE = 'app.models.CustomDjangoStorage'
SOCIAL_AUTH_GOOGLE_OAUTH_SCOPE = [
    'https://mail.google.com/',
    'https://www.googleapis.com/auth/userinfo.profile'
]
SOCIAL_AUTH_EMAIL_FORM_HTML = 'email_signup.html'
SOCIAL_AUTH_EMAIL_VALIDATION_FUNCTION = 'app.mail.send_validation'
SOCIAL_AUTH_EMAIL_VALIDATION_URL = '/email-sent/'
SOCIAL_AUTH_USERNAME_FORM_HTML = 'username_signup.html'

SOCIAL_AUTH_PIPELINE = (
    # Get the information we can about the user and return it in a simple
    # format to create the user instance later. On some cases the details are
    # already part of the auth response from the provider, but sometimes this
    # could hit a provider API.
    'social_core.pipeline.social_auth.social_details',

    # Get the social uid from whichever service we're authing thru. The uid is
    # the unique identifier of the given user in the provider.
    'social_core.pipeline.social_auth.social_uid',

    # Verifies that the current auth process is valid within the current
    # project, this is where emails and domains whitelists are applied (if
    # defined).
    'social_core.pipeline.social_auth.auth_allowed',

    # Checks if the current social-account is already associated in the site.
    'social_core.pipeline.social_auth.social_user',

    # ???
    'administration.pipeline.require_email',

    # Make up a username for this person, appends a random string at the end if
    # there's any collision.
    #'social_core.pipeline.user.get_username',

    # Send a validation email to the user to verify its email address.
    # Disabled by default.
    #'social_core.pipeline.mail.mail_validation', # TODO: fire an email to confirm auth

    # Associates the current social details with another user account with
    # a similar email address.
    'social_core.pipeline.social_auth.associate_by_email',

    # Create a user account if we haven't found one yet. DISABLED FOR MVP
    #'social_core.pipeline.user.create_user', #we're not creating any new users with this

    # Create the record that associates the social account with the user.
    'social_core.pipeline.social_auth.associate_user',

    # ???
    'social_core.pipeline.debug.debug',

    # Populate the extra_data field in the social record with the values
    # specified by settings (and the default ones like access_token, etc).
    'social_core.pipeline.social_auth.load_extra_data',

    # Update the user record with any changed info from the auth service.
    'social_core.pipeline.user.user_details',

    # ???
    'social_core.pipeline.debug.debug'
)

AUTHENTICATION_BACKENDS = (
    # Google OAuth2
    'social_core.backends.google.GoogleOAuth2',

    # django-rest-framework-social-oauth2
    'rest_framework_social_oauth2.backends.DjangoOAuth2',

    # Django
    'django.contrib.auth.backends.ModelBackend',
)

WSGI_APPLICATION = 'shakespeare.wsgi.application'



# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

## Used for REST API Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
        'rest_framework_social_oauth2.authentication.SocialAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

#APPEND_SLASH=False # We don't care if the user doesn't include the trailing slash

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

#STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "..", "www", "static")
STATIC_URL = '/static/'
