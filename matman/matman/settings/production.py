from .base import *

DEBUG = False

ADMINS = (
    ('Slarag', 'slarag@somemial.slarag'),
)

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
# SECURE_HSTS_SECONDS = 3600

SECRET_KEY = 'django-insecure-REPLACEME'