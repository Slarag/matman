"""
Password validators
"""

from django.core.exceptions import ValidationError


class SambaPwSetFakeValidator:
    """
    Fake Password Validator which can be used to access the plain-text password to use it for the samba user account.
    """

    def validate(self, password, user=None):
        return None

    def get_help_text(self):
        return ''

    def password_changed(self, password, user=None):
        # ToDo: Change samba password for user
        pass
