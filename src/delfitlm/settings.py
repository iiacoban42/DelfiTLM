"""
Django settings for delfitlm project.

Generated by 'django-admin startproject' using Django 3.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# gets the key from the runtime environment (docker-compose-deploy)
# change_me is default if a value is not specified
SECRET_KEY = os.environ.get('SECRET_KEY', 'change_me')
POSTGRES_DB         = os.environ.get('POSTGRES_DB', 'delfitlm')
POSTGRES_USER       = os.environ.get('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD   = os.environ.get('POSTGRES_PASSWORD', 'postgres')
POSTGRES_HOST       = os.environ.get('POSTGRES_HOST', 'localhost')
POSTGRES_PORT       = int(os.environ.get('POSTGRES_PORT', 5432))

# configure the email backend to relay email
EMAIL_BACKEND           = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST              = os.environ.get('SMTP_HOST', '')

if os.environ.get('SMTP_PORT') in ['', None]:
    EMAIL_PORT          = 25
else:
    EMAIL_PORT          = int(os.environ.get('SMTP_PORT'))

EMAIL_HOST_USER         = os.environ.get('SMTP_USER', '')
EMAIL_HOST_PASSWORD     = os.environ.get('SMTP_PASSWORD', '')
EMAIL_USE_TLS           = False
DEFAULT_FROM_EMAIL      = os.environ.get('FROM_EMAIL', 'webmaster@localhost')

if EMAIL_HOST == '':
    EMAIL_BACKEND       = 'django.core.mail.backends.console.EmailBackend'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.environ.get('DEBUG', 1)))

ALLOWED_HOSTS = []

# add allowed hosts specified in the environment
ALLOWED_HOSTS_ENV = os.environ.get('ALLOWED_HOSTS')
if ALLOWED_HOSTS_ENV:
    ALLOWED_HOSTS.extend(ALLOWED_HOSTS_ENV.split(','))

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'channels',
    'rest_framework',
    'rest_framework_api_key',
    'davinci',
    'delfic3',
    'delfin3xt',
    'delfipq',
    'transmission',
    'members',
    'home',
]

# REST_FRAMEWORK = {
#     "DEFAULT_PERMISSION_CLASSES": [
#         "rest_framework_api_key.permissions.HasAPIKey",
#     ]
# }

API_KEY_CUSTOM_HEADER = "HTTP_AUTHORIZATION"


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'delfitlm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'delfic3/templates'),
                 os.path.join(BASE_DIR, 'delfin3xt/templates'),
                 os.path.join(BASE_DIR, 'delfipq/templates'),
                 os.path.join(BASE_DIR, 'davinci/templates'),
                 os.path.join(BASE_DIR, 'members/templates'),
                 os.path.join(BASE_DIR, 'transmission/templates'),
                 os.path.join(BASE_DIR, 'home/templates')],
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

ASGI_APPLICATION = 'delfitlm.asgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': POSTGRES_DB,
        'USER': POSTGRES_USER,
        'PASSWORD': POSTGRES_PASSWORD,
        'HOST': POSTGRES_HOST,
        'PORT': POSTGRES_PORT,
    }
}

if 'test' in sys.argv or 'test_coverage' in sys.argv:  # Covers regular testing and django-coverage
    DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'members.Member'


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

STATIC_ROOT = '/vol/web/static'
MEDIA_ROOT = '/vol/web/media'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# prevent logger deadlock in debug mode
# in debug mode the server runs 2 processes that try to access the log files at the same time
if DEBUG and os.environ.get('RUN_MAIN', None) != 'true':
    LOGGING = {}

LOGGING = {
    'version': 1,
    'disable_existing_loggers' : False,
    'loggers': {
        'django_logger': {
            'handlers': ['debug_console', 'debug', 'info', 'warning', 'error', 'mail_admin'],
            'level': 1
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'std_err': {
            'class': 'logging.StreamHandler'
        },
        'debug_console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'default',
            # 'filters': ['require_debug_true'],
        },
        'debug': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/debug.log',
            'level': 'DEBUG',
            'formatter': 'default',
            'backupCount': 2,
            'maxBytes': 5*1024*1024, #bytes (5MB)
            'filters': ['require_debug_true'],

        },
        'info': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/info.log',
            'level': 'INFO',
            'formatter': 'default',
            'backupCount': 2,
            'maxBytes': 5*1024*1024,
        },
        'warning': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/warning.log',
            'level': 'WARNING',
            'formatter': 'default',
            'backupCount': 2,
            'maxBytes': 5*1024*1024,
        },
        'error': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/error.log',
            'level': 'ERROR',
            'formatter': 'error',
            'backupCount': 2,
            'maxBytes': 5*1024*1024,
        },
        'mail_admin': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'formatters': {
        'default': {
            'format': '%(asctime)s [%(module)s | %(levelname)s] %(message)s',
        },
        'error': {
            'format': '%(asctime)s [%(module)s | %(levelname)s] %(message)s @ %(pathname)s : %(lineno)d : %(funcName)s',
        },
    },
}
