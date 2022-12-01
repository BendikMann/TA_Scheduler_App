from django.test import TestCase

import random
import Factories
from faker import Faker
from TA_Scheduler.models import Account
from django.contrib.auth.models import Group
from TA_Scheduler.user import Admin, Instructor, Ta


class UserInitTests(TestCase):

    def setUp(self):
        self.fake = Faker()
        self.random_string = self.fake.word()
        self.random_integer = random.randint(0, 999999)

        self.blank_account = Factories.UserFactory.create().account
        self.blank_account.user.groups.clear()

        self.admin_account = Factories.UserFactory.create().account
        self.admin_account.user.groups.clear()
        self.admin_account.user.groups.add(Group.objects.get(name="Admin"))

        self.instructor_account = Factories.UserFactory.create().account
        self.instructor_account.user.groups.clear()
        self.instructor_account.user.groups.add(Group.objects.get(name="Instructor"))

        self.ta_account = Factories.UserFactory.create().account
        self.ta_account.user.groups.clear()
        self.ta_account.user.groups.add(Group.objects.get(name="TA"))

        self.admin_instructor_account: Account = Factories.UserFactory.create().account
        self.admin_instructor_account.user.groups.clear()
        self.admin_instructor_account.user.groups.add(Group.objects.get(name="Admin"))
        self.admin_instructor_account.user.groups.add(Group.objects.get(name="Instructor"))

        self.ta_instructor_account: Account = Factories.UserFactory.create().account
        self.ta_instructor_account.user.groups.clear()
        self.ta_instructor_account.user.groups.add(Group.objects.get(name="TA"))
        self.ta_instructor_account.user.groups.add(Group.objects.get(name="Instructor"))

        self.admin_ta_account: Account = Factories.UserFactory.create().account
        self.admin_ta_account.user.groups.clear()
        self.admin_ta_account.user.groups.add(Group.objects.get(name="Admin"))
        self.admin_ta_account.user.groups.add(Group.objects.get(name="TA"))

    def test_admin_init(self):
        try:
            a = Admin(self.admin_account)
        except TypeError:
            self.fail("Admin __init__ raised TypeError when Admin Account was passed")
        except ValueError:
            self.fail("Admin __init__ raised ValueError when Admin Account was passed")

    def test_admin_init_wrong_type(self):
        with self.assertRaises(TypeError, msg="TypeError not raised when passing Admin __init__ a string"):
            a = Admin(self.random_string)

        with self.assertRaises(TypeError, msg="TypeError not raised when passing Admin __init__ an integer"):
            a = Admin(self.random_integer)

    def test_admin_init_wrong_account_group(self):
        with self.assertRaises(ValueError, msg="ValueError not raised when passing Admin __init__ an account with no "
                                               "group"):
            a = Admin(self.blank_account)

        with self.assertRaises(ValueError, msg="ValueError not raised when passing Admin __init__ an account only in "
                                               "TA group"):
            a = Admin(self.ta_account)

        with self.assertRaises(ValueError, msg="ValueError not raised when passing Admin __init__ an account only in "
                                               "Instructor group"):
            a = Admin(self.instructor_account)

    def test_admin_init_mult_groups(self):
        try:
            a = Admin(self.admin_instructor_account)
            a = Admin(self.admin_ta_account)
        except TypeError:
            self.fail("Admin __init__ raised TypeError when account with multiple groups (Admin included) was passed")
        except ValueError:
            self.fail("Admin __init__ raised ValueError when account with multiple groups (Admin included) was passed")

        with self.assertRaises(ValueError, msg="ValueError not raised when passing Admin __init__ an account with "
                                               "multiple invalid groups"):
            a = Admin(self.ta_instructor_account)

    def test_instructor_init(self):
        try:
            a = Instructor(self.instructor_account)
        except TypeError:
            self.fail("Instructor __init__ raised TypeError when Instructor Account was passed")
        except ValueError:
            self.fail("Instructor __init__ raised ValueError when Instructor Account was passed")

    def test_instructor_init_wrong_type(self):
        with self.assertRaises(TypeError, msg="TypeError not raised when passing Instructor __init__ a string"):
            a = Instructor(self.random_string)

        with self.assertRaises(TypeError, msg="TypeError not raised when passing Instructor __init__ an integer"):
            a = Instructor(self.random_integer)

    def test_instructor_init_wrong_account_group(self):
        with self.assertRaises(ValueError, msg="ValueError not raised when passing Instructor __init__ an account "
                                               "with no group"):
            a = Instructor(self.blank_account)

        with self.assertRaises(ValueError, msg="ValueError not raised when passing Instructor __init__ an account "
                                               "only in TA group"):
            a = Instructor(self.ta_account)

        with self.assertRaises(ValueError, msg="ValueError not raised when passing Instructor __init__ an account "
                                               "only in Admin group"):
            a = Instructor(self.admin_account)

    def test_instructor_init_mult_groups(self):
        try:
            a = Instructor(self.admin_instructor_account)
            a = Instructor(self.ta_instructor_account)
        except TypeError:
            self.fail("Instructor __init__ raised TypeError when account with multiple groups (Instructor included) "
                      "was passed")
        except ValueError:
            self.fail("Instructor __init__ raised ValueError when account with multiple groups (Instructor included) "
                      "was passed")

        with self.assertRaises(ValueError, msg="ValueError not raised when passing Instructor __init__ an account with "
                                               "multiple invalid groups"):
            a = Instructor(self.admin_ta_account)

    def test_ta_init(self):
        try:
            a = Ta(self.ta_account)
        except TypeError:
            self.fail("Ta __init__ raised TypeError when Ta Account was passed")
        except ValueError:
            self.fail("Ta __init__ raised ValueError when Ta Account was passed")

    def test_ta_init_wrong_type(self):
        with self.assertRaises(TypeError, msg="TypeError not raised when passing Ta __init__ a string"):
            a = Ta(self.random_string)

        with self.assertRaises(TypeError, msg="TypeError not raised when passing Ta __init__ an integer"):
            a = Ta(self.random_integer)

    def test_ta_init_wrong_account_group(self):
        with self.assertRaises(ValueError, msg="ValueError not raised when passing Ta __init__ an account with no "
                                               "group"):
            a = Ta(self.blank_account)

        with self.assertRaises(ValueError, msg="ValueError not raised when passing Ta __init__ an account only in "
                                               "Admin group"):
            a = Ta(self.admin_account)

        with self.assertRaises(ValueError, msg="ValueError not raised when passing Ta __init__ an account only in "
                                               "Instructor group"):
            a = Ta(self.instructor_account)

    def test_ta_init_mult_groups(self):
        try:
            a = Ta(self.admin_ta_account)
            a = Ta(self.ta_instructor_account)
        except TypeError:
            self.fail("Ta __init__ raised TypeError when account with multiple groups (Ta included) was passed")
        except ValueError:
            self.fail("Ta __init__ raised ValueError when account with multiple groups (Ta included) was passed")

        with self.assertRaises(ValueError, msg="ValueError not raised when passing Ta __init__ an account with "
                                               "multiple invalid groups"):
            a = Ta(self.admin_instructor_account)
