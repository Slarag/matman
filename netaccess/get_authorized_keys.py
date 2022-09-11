"""
Script for retrieving authorized keys for a given user from the netaccess db.

To be used for AuthorizedKeysCommand in sshd_config.
"""

import argparse
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "netaccess.settings")

import django
django.setup()
from django.contrib.auth.models import User


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('user', help='The username to look up authorized keys for.')
    args = parser.parse_args()

    # print(settings.AUTH_USER_MODEL)

    # user = settings.AUTH_USER_MODEL.objects.filter(username=args.user)
    user = User.objects.filter(username=args.user)[0]

    if user is not None:
        print('\n'.join(pk.to_authorized_keys_line() for pk in user.pubkeys.all()))
