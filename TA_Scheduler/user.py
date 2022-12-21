from typing import Union
from django.core.mail import send_mail
from typing import Union

from django.contrib.auth.models import Group
from TA_Scheduler.models import User, Course
from django.core.mail import send_mail

class Admin:
    """
    Wraps the User with the assumption it is an admin.
    """

    def __init__(self, account: User):
        """
        :param account: Account to wrap as an admin. Must be an admin, otherwise raise exception.
        """
        if not (isinstance(account, User)):
            raise TypeError('Instance supplied to Admin constructor is not an account')

        if not is_admin(account):
            raise ValueError('Account supplied to Admin constructor is not in the Admin group')

        self.account = account

    def send_email(self, header: str, content: str) -> bool:
        # Gets a list of all user emails excluding blank ones
        emails = list(User.objects.filter(is_active=True).exclude(email='').values_list('email', flat=True))
        send_mail(subject=header, message=content, from_email='NYStingers@ta-scheduler.rocks', recipient_list=emails)
        # returns the recipients of the email
        return emails


class Ta:
    def __init__(self, account: User):
        """
        :param account: Account to wrap as an TA. Must be a TA, otherwise raise exception.
        """
        if not (isinstance(account, User)):
            raise TypeError('Instance supplied to Ta constructor is not an account')

        if not is_ta(account):
            raise ValueError('Account supplied to Ta constructor is not in the TA group')

        self.account = account


class Instructor:
    def __init__(self, account: User):
        """
        :param account: Account to wrap as an admin. Must be an admin, otherwise raise exception.
        """
        if not (isinstance(account, User)):
            raise TypeError('Instance supplied to Instructor constructor is not an account')

        if not is_instructor(account):
            raise ValueError('Account supplied to Instructor constructor is not in the Instructor group')

        self.account = account

    def send_email(self, header: str, content: str) -> bool:
        # Gets a list of all user emails excluding blank ones
        tas = self.get_assigned_tas()
        emails = []
        # Gets a list of all the emails of the TA's that are assigned to a specific instructor
        for ta in tas:
            emails.append(ta.email)
        send_mail(subject=header, message=content, from_email='NYStingers@ta-scheduler.rocks', recipient_list=emails)
        # returns the recipients of the email
        return emails

    def get_assigned_tas(self):
        # Courses that our instructor is in
        course_list = list(Course.objects.filter(assigned_people__id=self.account.id))
        # a list that will contain all the users that share a course with the instructor including the instructor
        all_users_in_courses = []
        # the final list that will contain the TA's that share a course with the instructor
        ta_list = []
        for course in course_list:
            # each course get all users and add them to a list
            all_users_in_courses.append(list(course.assigned_people.all()))
        for users in all_users_in_courses:
            for user in users:
                # check if a user is not a ta or is already in the new list
                if is_ta(user) and user not in ta_list:
                    ta_list.append(user)
        return ta_list



def get_all_instructors() -> list[Instructor]:
    """

    :return: All instructors in the Instructor group.
    """

    return list(User.objects.all().filter(groups__name='Instructor'))


def get_all_admins() -> list[Admin]:
    """

    :return: All Admins in the admin group.
    """

    return list(User.objects.all().filter(groups__name='Admin'))


def get_all_users() -> list[User]:
    accounts = list(User.objects.all())
    return accounts


def get_all_tas() -> list[Ta]:
    """

    :return: All users in the Ta group.
    """
    return list(User.objects.all().filter(groups__name='TA'))


def is_admin(account: User) -> bool:
    """

    :param account:
    :return: True if account is in admin group, False if account is not in admin group
    """
    if not (isinstance(account, User)):
        raise TypeError('Instance supplied to is_admin is not an account')

    return account.groups.filter(name='Admin').exists()


def is_instructor(account: User) -> bool:
    """

    :param account: The account to check.
    :return: True if account is in instructor group, False if account is not in instructor group
    """
    if not (isinstance(account, User)):
        raise TypeError('Instance supplied to is_instructor is not an account')

    return account.groups.filter(name='Instructor').exists()


def is_ta(account: User) -> bool:
    """

    :param account: The account to check
    :return: True if the account is in TA group, False if account is not in TA group
    """
    if not (isinstance(account, User)):
        raise TypeError('Instance supplied to is_ta is not an account')

    return account.groups.filter(name='TA').exists()


def make_admin(account: User) -> Union[Admin, None]:
    """
    Makes the specified Account an Admin.
    :param account: The Account Model to make admin.
    :return: The Admin instance if account was made admin or was already Admin, None otherwise.
    """
    if not (isinstance(account, User)):
        raise TypeError('Instance supplied to make_admin is not an account')

    if not is_admin(account):
        account.groups.add(Group.objects.get(name="Admin"))

    return Admin(account)


def make_instructor(user: User) -> Union[Instructor, None]:
    """
    Makes the specified Account an Instructor
    :param user: The Account Model to make instructor
    :return: The Instructor instance if account was made instructor or was already instructor, None otherwise.
    """
    if not (isinstance(user, User)):
        raise TypeError('Instance supplied to make_instructor is not an account')

    if is_ta(user):
        return None

    if not is_instructor(user):
        user.groups.add(Group.objects.get(name="Instructor"))

    return Instructor(user)


def make_ta(user: User) -> Union[Ta, None]:
    """
    Makes the specified Account a TA
    :param user: The Account Model to make TA
    :return: The TA instance if account was made TA or was already TA, None otherwise.
    """
    if not (isinstance(user, User)):
        raise TypeError('Instance supplied to make_ta is not an account')

    if is_instructor(user):
        return None

    if not is_ta(user):
        user.groups.add(Group.objects.get(name="TA"))

    return Ta(user)

