from .base import *

DEBUG = True

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