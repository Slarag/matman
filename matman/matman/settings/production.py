from .base import *


def env_getboolean(varname: str, default: bool = False) -> bool:
    return os.environ.get(varname, 'true' if default else 'false').lower() in ('true', '1', 'yes', 'on')


# Read SECRET_KEY from an environment variable
SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = False

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['POSTGRES_DB_NAME'],
        'USER': os.environ['POSTGRES_USER'],
        'PASSWORD': os.environ['POSTGRES_PASSWORD'],
        'HOST': 'db',
        'PORT': 5432
        ,
    }
}

CSRF_COOKIE_SECURE = env_getboolean('CSRF_COOKIE_SECURE', True)
SESSION_COOKIE_SECURE = env_getboolean('SESSION_COOKIE_SECURE', True)
SECURE_SSL_REDIRECT = env_getboolean('SECURE_SSL_REDIRECT', True)
# SECURE_HSTS_SECONDS = 3600

# Mail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = env_getboolean('EMAIL_USE_TLS', False)
EMAIL_USE_SSL = env_getboolean('EMAIL_USE_SSL', True)
EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '465'))
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
DEFAULT_FROM_EMAIL = os.environ['DEFAULT_FROM_EMAIL']
EMAIL_SUBJECT_PREFIX = 'MatMan - '

ALLOW_REGISTRATION = env_getboolean('ALLOW_REGISTRATION', False)
ALLOW_CHANGE_PASSWORD = env_getboolean('ALLOW_CHANGE_PASSWORD', False)
ALLOW_RESET_PASSWORD = env_getboolean('ALLOW_RESET_PASSWORD', False)

SITE_ID = 1
