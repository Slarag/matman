from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-3!-4+z^xnm5nl7t=+0n!&l!t6ftx7sqdzu*=rw@s+a^i&diho2'