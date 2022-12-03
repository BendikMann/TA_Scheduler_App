import abc
from TA_Scheduler.models import Account, Course, Lab
from TA_Scheduler.account_util import is_admin, is_instructor, is_ta


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


def get_all_tas() -> list[Ta]:
    """

    :return: All users in the Ta group.
    """
    pass


def get_all_instructors() -> list[Instructor]:
    """

    :return: All instructors in the Instructor group.
    """
    pass


def get_all_admins() -> list[Admin]:
    """

    :return: All Admins in the admin group.
    """

    pass
