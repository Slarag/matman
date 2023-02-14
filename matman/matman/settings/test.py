from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
SECRET_KEY = 'django-insecure-changeme'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/
LANGUAGE_CODE = 'en-en'
TIME_ZONE = 'GMT'
USE_I18N = False
USE_TZ = True

# Security
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False

# Email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# login and registration config
ALLOW_REGISTRATION = True
ALLOW_CHANGE_PASSWORD = True
ALLOW_RESET_PASSWORD = True

# Celery Configuration Options
CELERY_TIMEZONE = "Europe/Berlin"

