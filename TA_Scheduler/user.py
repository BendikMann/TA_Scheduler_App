from typing import Union
from TA_Scheduler.models import Account, Course, Lab
from TA_Scheduler.models import Account, UsAddress


class Admin:
    """
    Wraps the User with the assumption it is an admin.
    """

    def __init__(self, account: Account):
        """
        :param account: Account to wrap as an admin. Must be an admin, otherwise raise exception.
        """
        if not (isinstance(account, Account)):
            raise TypeError('Instance supplied to Admin constructor is not an account')

        if not is_admin(account):
            raise ValueError('Account supplied to Admin constructor is not in the Admin group')

        self.account = account

    def send_email(self, header: str, content: str) -> bool:
        """
        Sends an email to all Accounts with header: header and content content.
        :param header:
        :param content:
        :return: True if the email was succesfully sent, false otherwise.
        """
        pass

    pass


class Ta:
    def __init__(self, account: Account):
        """
        :param account: Account to wrap as an TA. Must be a TA, otherwise raise exception.
        """
        if not (isinstance(account, Account)):
            raise TypeError('Instance supplied to Ta constructor is not an account')

        if not is_ta(account):
            raise ValueError('Account supplied to Ta constructor is not in the TA group')

        self.account = account

    def assign_instructor(self, instructor: "Instructor") -> bool:
        """
        Assigns this ta to the specified instructor.
        :param instructor:
        :return: True if the instructor is or has had the ta assigned to the ta. False otherwise
        """

        pass

    def remove_instructor(self, instructor: "Instructor") -> bool:
        """
        Removes the assignment of this ta to the specified instructor.
        :param instructor:  True if the ta is or has been removed from the ta. False otherwise.
        :return:
        """
        pass

    def assign_lab_section(self, lab_section: Lab) -> bool:
        pass

    def remove_lab_section(self, lab_section: Lab) -> bool:
        pass

    def get_courses(self) -> list[Course]:
        pass

    def get_lab_sections(self) -> list[Lab]:
        pass


class Instructor:
    def __init__(self, account: Account):
        """
        :param account: Account to wrap as an admin. Must be an admin, otherwise raise exception.
        """
        if not (isinstance(account, Account)):
            raise TypeError('Instance supplied to Instructor constructor is not an account')

        if not is_instructor(account):
            raise ValueError('Account supplied to Instructor constructor is not in the Instructor group')

        self.account = account

    def assign_course(self, course: Course) -> bool:
        pass

    def remove_course(self, course: Course) -> bool:
        pass

    def get_courses(self) -> list[Course]:
        pass

    def assign_ta(self, ta: Ta) -> bool:
        pass

    def remove_ta(self, ta: Ta) -> bool:
        pass

    def get_assigned_tas(self) -> list[Ta]:
        pass

    def send_email(self, header: str, content: str) -> bool:
        """
        Sends an email to all Ta's of the instructor with header: header and content: content.
        :param header:
        :param content:
        :return: True if the email was successfully sent, false otherwise.
        """
        pass


def get_all_instructors() -> list[Instructor]:
    """

    :return: All instructors in the Instructor group.
    """

    return list(Account.objects.all().filter(user__groups__name='Instructor'))


def get_all_admins() -> list[Admin]:
    """

    :return: All Admins in the admin group.
    """

    return list(Account.objects.all().filter(user__groups__name='Admin'))


def get_all_users() -> list[Account]:
    return list(Account.objects.all())


def get_all_tas() -> list[Ta]:
    """

    :return: All users in the Ta group.
    """
    return list(Account.objects.all().filter(user__groups__name='TA'))


def is_admin(account: Account) -> bool:
    """

    :param account:
    :return: True if account is in admin group, False if account is not in admin group
    """
    if not (isinstance(account, Account)):
        raise TypeError('Instance supplied to is_admin is not an account')

    return account.user.groups.filter(name='Admin').exists()


def is_instructor(account: Account) -> bool:
    """

    :param account: The account to check.
    :return: True if account is in instructor group, False if account is not in instructor group
    """
    if not (isinstance(account, Account)):
        raise TypeError('Instance supplied to is_instructor is not an account')

    return account.user.groups.filter(name='Instructor').exists()


def is_ta(account: Account) -> bool:
    """

    :param account: The account to check
    :return: True if the account is in TA group, False if account is not in TA group
    """
    if not (isinstance(account, Account)):
        raise TypeError('Instance supplied to is_ta is not an account')

    return account.user.groups.filter(name='TA').exists()


def make_admin(account: Account) -> Union[Admin, None]:
    """
    Makes the specified Account an Admin.
    :param account: The Account Model to make admin.
    :return: The Admin instance if account was made admin or was already Admin, None otherwise.
    """
    if not (isinstance(account, Account)):
        raise TypeError('Instance supplied to make_admin is not an account')
    pass


def make_instructor(account: Account) -> Union[Instructor, None]:
    """
    Makes the specified Account an Instructor
    :param account: The Account Model to make instructor
    :return: The Instructor instance if account was made instructor or was already instructor, None otherwise.
    """
    if not (isinstance(account, Account)):
        raise TypeError('Instance supplied to make_instructor is not an account')
    pass


def make_ta(account: Account) -> Union[Ta, None]:
    """
    Makes the specified Account a TA
    :param account: The Account Model to make TA
    :return: The TA instance if account was made TA or was already TA, None otherwise.
    """
    if not (isinstance(account, Account)):
        raise TypeError('Instance supplied to make_ta is not an account')
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
