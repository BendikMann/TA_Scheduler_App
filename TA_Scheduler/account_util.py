from typing import Union
from django.contrib.auth.models import User

from TA_Scheduler.user import *
from TA_Scheduler.models import Account, UsAddress


def is_admin(account: Account) -> bool:
    """

    :param account:
    :return: True if account is in admin group.
    """
    pass


def make_admin(account: Account) -> Union[Admin, None]:
    """
    Makes the specified Account an Admin.
    :param account: The Account Model to make admin.
    :return: The Admin instance if account was made admin or was already Admin, None otherwise.
    """
    pass


def is_instructor(account: Account) -> bool:
    """

    :param account: The account to check.
    :return: True if account is in instructor group.
    """
    pass


def make_instructor(account: Account) -> Union[Instructor, None]:
    """
    Makes the specified Account an Instructor
    :param account: The Account Model to make instructor
    :return: The Instructor instance if account was made instructor or was already instructor, None otherwise.
    """
    pass


def is_ta(account: Account) -> bool:
    """

    :param account: The account to check
    :return: True if the account is in TA group.
    """
    pass


def make_ta(account: Account) -> Union[Ta, None]:
    """
    Makes the specified Account a TA
    :param account: The Account Model to make TA
    :return: The TA instance if account was made TA or was already TA, None otherwise.
    """
    pass


def create_account(username: str,
                   first_name: str,
                   last_name: str,
                   email: str,
                   password: str,
                   address: UsAddress,
                   phone_number: str) -> Union[Account, None]:
    """
    Attempts to create an account with the given parameters.
    :param username:
    :param first_name:
    :param last_name:
    :param email:
    :param password:
    :param address:
    :param phone_number:
    :return: The Account created on success, None otherwise.
    """
    pass


def delete_account(account: Account):
    """
    :param account: Account to delete
    :return: True if the account was successfully deleted, false otherwise.
    """
    pass
