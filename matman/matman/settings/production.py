import os

from .base import *

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.DB_PASSWORD['POSTGRES_PASSWORD'],
        'HOST': 'db',
        'PORT': 5423,
    }
}

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/
LANGUAGE_CODE = 'en-en'
TIME_ZONE = os.environ.get('TIME_ZONE', 'GMT')
USE_I18N = False
USE_TZ = 'true'

# Celery Configuration Options
CELERY_TIMEZONE = os.environ.get('CELERY_TIMEZONE', 'Europe/Berlin')

# login and registration config
ALLOW_REGISTRATION = os.environ.get('ALLOW_REGISTRATION', '').lower() == 'true'
ALLOW_CHANGE_PASSWORD = os.environ.get('ALLOW_CHANGE_PASSWORD', '').lower() == 'true'
ALLOW_RESET_PASSWORD = os.environ.get('ALLOW_RESET_PASSWORD', '').lower() == 'true'

# Security
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
# SECURE_HSTS_SECONDS = 3600

# Read SECRET_KEY from an environment variable
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

EMAIL_USE_TLS = os.environ.get('ALLOW_REGISTRATION', 'EMAIL_USE_TLS').lower() == 'true'
EMAIL_HOST = os.environ.get('ALLOW_REGISTRATION', 'EMAIL_HOST').lower() == 'true'
EMAIL_PORT = os.environ.get('ALLOW_REGISTRATION', 'EMAIL_PORT').lower() == 'true'
EMAIL_HOST_USER = os.environ.get('ALLOW_REGISTRATION', 'EMAIL_HOST_USER').lower() == 'true'
EMAIL_HOST_PASSWORD = os.environ.get('ALLOW_REGISTRATION', 'EMAIL_HOST_PASSWORD').lower() == 'true'

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_BACKEND")
