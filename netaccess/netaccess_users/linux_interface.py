"""
Functions for controlling linux system users and groups as well as samba user accounts.
"""

from typing import List
import grp
import pwd
import subprocess


def user_exits(user: str) -> bool:
    """
    Check if Linux system user exists on the local system.

    :param user: Name of the user to be looked up.
    :return:  True, if the given user exits, otherwise false.
    """

    try:
        pwd.getpwnam(user)
    except KeyError:
        return False
    else:
        return True


def user_add(user: str, groups: List[str]) -> bool:
    """
    Add a Linux system user without user group and no login-shell.

    :param user: Name of the user to be created.
    :param groups: List of groups the user should be added to.
    :return: True, if the user was successfully created, otherwise false.
    """

    try:
        subprocess.run(['useradd', '-g', ','.join(groups), '--no-user-group', '-s', '/usr/sbin/nologin', user],
                       check=True)
        return True
    except subprocess.CalledProcessError:
        # Could not create user
        return False


def user_delete(user: str) -> bool:
    """
    Delete an existing Linux system user.

    :param user: Name of the user to be deleted.
    :return: True, if the user was successfully deleted, otherwise false.
    """

    try:
        subprocess.run(['userdel', user], check=True)
        return True
    except subprocess.CalledProcessError:
        # Could not delete user
        return False


def group_exits(group: str) -> bool:
    """
    Check if Linux user group exists on the local system.

    :param group: Name of the group to be looked up.
    :return: True, if the given group exits, otherwise false.
    """

    try:
        grp.getgrnam(group)
    except KeyError:
        return False
    else:
        return True


def group_add(group: str) -> bool:
    """
    Create/add a Linux user group.

    :param group: Name of the group to be created.
    :return: True, if the group was successfully created, otherwise false.
    """

    try:
        subprocess.run(['groupadd', group],
                       check=True)
        return True
    except subprocess.CalledProcessError:
        # Could not create group
        return False


def group_delete(user: str) -> bool:
    """
    Delete an existing Linux user group.

    :param user: Name of the group to be deleted.
    :return: True, if the group was successfully deleted, otherwise false.
    """

    try:
        subprocess.run(['groupdel', user], check=True)
        return True
    except subprocess.CalledProcessError:
        # Could not delete group
        return False


def is_group_member(user: str, group: str) -> bool:
    """
    Check if a given system user exits and is a member of a given group.

    :param user: Name of the user to be looked up.
    :param group: Name of the group to be looked up.
    :return: True, if both group and user exist and the user is a member of the group, otherwise False.
    """

    if not user_exits(user) or not group_exits(group):
        return False
    return user in grp.getgrnam(group).gr_mem


def samba_add_user(username: str, pw: str) -> bool:
    """
    Add an existing system user to the Samba database.

    :param username: Name of the user to be added.
    :param pw: Samba password to be assigned to the user.
    :return: True, if the user was successfully added to the Samba database, otherwise False.
    """

    try:
        subprocess.run(['smbpasswd', '-a', username], input=f'{pw}\n{pw}\n',
                       encoding='utf-8', errors='ignore', check=True)
        return True
    except subprocess.CalledProcessError:
        # Could not add user
        return False


def samba_change_pw(username: str, pw: str) -> bool:
    """
    Change Samba password for a given user.

    :param username: Name of the user.
    :param pw: New Samba password to be assigned to the user.
    :return: True, if the Samba password was successfully changed, otherwise False.
    """

    try:
        subprocess.run(['smbpasswd', username], input=f'{pw}\n{pw}\n', encoding='utf-8', errors='ignore', check=True)
        return True
    except subprocess.CalledProcessError:
        # Could not add user
        return False


def samba_delete_user(username: str) -> bool:
    """
    Delete user from the Samba database.

    :param username: Name of the user.
    :return: True, if the user was successfully removed from the Samba database, otherwise False.
    """

    try:
        subprocess.run(['smbpasswd', '-x', username], check=True)
        return True
    except subprocess.CalledProcessError:
        # Could not add user
        return False


def samba_disable_user(username: str) -> bool:
    """
    Disable user in the Samba database.

    :param username: Name of the user.
    :return: True, if the user was successfully disabled in the Samba database, otherwise False.
    """

    try:
        subprocess.run(['smbpasswd', '-d', username], check=True)
        return True
    except subprocess.CalledProcessError:
        # Could not add user
        return False


def samba_enable_user(username: str) -> bool:
    """
    Enable user in the Samba database.

    :param username: Name of the user.
    :return: True, if the user was successfully enabled in the Samba database, otherwise False.
    """

    try:
        subprocess.run(['smbpasswd', '-e', username], check=True)
        return True
    except subprocess.CalledProcessError:
        # Could not add user
        return False

