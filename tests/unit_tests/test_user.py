from django.core import mail
from django.test import TestCase
from tests.Factories import *
from TA_Scheduler import user
import random
from faker import Faker
from TA_Scheduler.models import User
from django.contrib.auth.models import Group
from TA_Scheduler.user import Admin, Instructor, Ta, is_ta


def init_dummy_database():
    """
    Creates a db with 50 users, 10 courses and 20 labs.
    All randomly linked in legal (and logical) ways.
    """
    for i in range(0, 50):
        UserFactory(password="not_signinable")

    for i in range(0, 10):
        CourseFactory()


class UserInitTests(TestCase):

    def setUp(self):
        self.fake = Faker()
        self.random_string = self.fake.word()
        self.random_integer = random.randint(0, 999999)

        self.blank_account = UserFactory.create()
        self.blank_account.groups.clear()

        self.admin_account = UserFactory.create()
        self.admin_account.groups.clear()
        self.admin_account.groups.add(Group.objects.get(name="Admin"))

        self.instructor_account = UserFactory.create()
        self.instructor_account.groups.clear()
        self.instructor_account.groups.add(Group.objects.get(name="Instructor"))

        self.ta_account = UserFactory.create()
        self.ta_account.groups.clear()
        self.ta_account.groups.add(Group.objects.get(name="TA"))

        self.admin_instructor_account: User = UserFactory.create()
        self.admin_instructor_account.groups.clear()
        self.admin_instructor_account.groups.add(Group.objects.get(name="Admin"))
        self.admin_instructor_account.groups.add(Group.objects.get(name="Instructor"))

        self.ta_instructor_account: User = UserFactory.create()
        self.ta_instructor_account.groups.clear()
        self.ta_instructor_account.groups.add(Group.objects.get(name="TA"))
        self.ta_instructor_account.groups.add(Group.objects.get(name="Instructor"))

        self.admin_ta_account: User = UserFactory.create()
        self.admin_ta_account.groups.clear()
        self.admin_ta_account.groups.add(Group.objects.get(name="Admin"))
        self.admin_ta_account.groups.add(Group.objects.get(name="TA"))

    def test_admin_init(self):
        try:
            a = Admin(self.admin_account)
            self.assertEqual(a.account, self.admin_account)
        except TypeError:
            self.fail("Admin __init__ raised TypeError when Admin Account was passed")
        except ValueError:
            self.fail("Admin __init__ raised ValueError when Admin Account was passed")

    def test_admin_init_wrong_type(self):
        with self.assertRaises(TypeError, msg="TypeError not raised when passing Admin __init__ a string"):
            a = Admin(self.random_string)

        with self.assertRaises(TypeError, msg="TypeError not raised when passing Admin __init__ an integer"):
            b = Admin(self.random_integer)

    def test_admin_init_wrong_account_group(self):
        with self.assertRaises(ValueError, msg="ValueError not raised when passing Admin __init__ an account with no "
                                               "group"):
            a = Admin(self.blank_account)

        with self.assertRaises(ValueError, msg="ValueError not raised when passing Admin __init__ an account only in "
                                               "TA group"):
            b = Admin(self.ta_account)

        with self.assertRaises(ValueError, msg="ValueError not raised when passing Admin __init__ an account only in "
                                               "Instructor group"):
            c = Admin(self.instructor_account)

    def test_admin_init_mult_groups(self):
        try:
            a = Admin(self.admin_instructor_account)
            b = Admin(self.admin_ta_account)
            self.assertEqual(a.account, self.admin_instructor_account)
            self.assertEqual(b.account, self.admin_ta_account)
        except TypeError:
            self.fail("Admin __init__ raised TypeError when account with multiple groups (Admin included) was passed")
        except ValueError:
            self.fail("Admin __init__ raised ValueError when account with multiple groups (Admin included) was passed")

        with self.assertRaises(ValueError, msg="ValueError not raised when passing Admin __init__ an account with "
                                               "multiple invalid groups"):
            c = Admin(self.ta_instructor_account)

    def test_instructor_init(self):
        try:
            a = Instructor(self.instructor_account)
            self.assertEqual(a.account, self.instructor_account)
        except TypeError:
            self.fail("Instructor __init__ raised TypeError when Instructor Account was passed")
        except ValueError:
            self.fail("Instructor __init__ raised ValueError when Instructor Account was passed")

    def test_instructor_init_wrong_type(self):
        with self.assertRaises(TypeError, msg="TypeError not raised when passing Instructor __init__ a string"):
            a = Instructor(self.random_string)

        with self.assertRaises(TypeError, msg="TypeError not raised when passing Instructor __init__ an integer"):
            b = Instructor(self.random_integer)

    def test_instructor_init_wrong_account_group(self):
        with self.assertRaises(ValueError, msg="ValueError not raised when passing Instructor __init__ an account "
                                               "with no group"):
            a = Instructor(self.blank_account)

        with self.assertRaises(ValueError, msg="ValueError not raised when passing Instructor __init__ an account "
                                               "only in TA group"):
            b = Instructor(self.ta_account)

        with self.assertRaises(ValueError, msg="ValueError not raised when passing Instructor __init__ an account "
                                               "only in Admin group"):
            c = Instructor(self.admin_account)

    def test_instructor_init_mult_groups(self):
        try:
            a = Instructor(self.admin_instructor_account)
            b = Instructor(self.ta_instructor_account)
            self.assertEqual(a.account, self.admin_instructor_account)
            self.assertEqual(b.account, self.ta_instructor_account)
        except TypeError:
            self.fail("Instructor __init__ raised TypeError when account with multiple groups (Instructor included) "
                      "was passed")
        except ValueError:
            self.fail("Instructor __init__ raised ValueError when account with multiple groups (Instructor included) "
                      "was passed")

        with self.assertRaises(ValueError, msg="ValueError not raised when passing Instructor __init__ an account with "
                                               "multiple invalid groups"):
            c = Instructor(self.admin_ta_account)

    def test_ta_init(self):
        try:
            a = Ta(self.ta_account)
            self.assertEqual(a.account, self.ta_account)
        except TypeError:
            self.fail("Ta __init__ raised TypeError when Ta Account was passed")
        except ValueError:
            self.fail("Ta __init__ raised ValueError when Ta Account was passed")

    def test_ta_init_wrong_type(self):
        with self.assertRaises(TypeError, msg="TypeError not raised when passing Ta __init__ a string"):
            a = Ta(self.random_string)

        with self.assertRaises(TypeError, msg="TypeError not raised when passing Ta __init__ an integer"):
            b = Ta(self.random_integer)

    def test_ta_init_wrong_account_group(self):
        with self.assertRaises(ValueError, msg="ValueError not raised when passing Ta __init__ an account with no "
                                               "group"):
            a = Ta(self.blank_account)

        with self.assertRaises(ValueError, msg="ValueError not raised when passing Ta __init__ an account only in "
                                               "Admin group"):
            b = Ta(self.admin_account)

        with self.assertRaises(ValueError, msg="ValueError not raised when passing Ta __init__ an account only in "
                                               "Instructor group"):
            c = Ta(self.instructor_account)

    def test_ta_init_mult_groups(self):
        try:
            a = Ta(self.admin_ta_account)
            b = Ta(self.ta_instructor_account)
            self.assertEqual(a.account, self.admin_ta_account)
            self.assertEqual(b.account, self.ta_instructor_account)
        except TypeError:
            self.fail("Ta __init__ raised TypeError when account with multiple groups (Ta included) was passed")
        except ValueError:
            self.fail("Ta __init__ raised ValueError when account with multiple groups (Ta included) was passed")

        with self.assertRaises(ValueError, msg="ValueError not raised when passing Ta __init__ an account with "
                                               "multiple invalid groups"):
            c = Ta(self.admin_instructor_account)


class Test_Get_All_Tas(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
            Creates a db with 50 users, 10 courses and 20 labs.
            All randomly linked in legal (and logical) ways.
            """
        for i in range(0, 50):
            UserFactory(password="sdfasfasdf")

        for i in range(0, 10):
            CourseFactory()

    def test_actually_returns_valid(self):
        self.assertIsInstance(user.get_all_tas(), list,
                              msg=f"Get all should return list, returned {type(user.get_all_tas())}")

    def test_count_correct(self):
        tas = models.User.objects.filter(groups__name="TA")

        list_tas: list[user.Ta] = user.get_all_tas()

        self.assertIsNotNone(list_tas, msg="Should return empty list instead!")
        self.assertEqual(len(tas), len(list_tas),
                         msg=f"All tas should include all tas in the db. Actual: {len(tas)} Is {len(list_tas)}")

    def test_exhaustive(self):
        tas = list(models.User.objects.filter(groups__name="TA").all())
        tas = sorted(tas, key=lambda x: x.email)
        list_tas: list[user.Ta] = user.get_all_tas()
        list_tas = sorted(tas, key=lambda x: x.email)

        for i in range(0, min(len(tas), len(list_tas))):
            self.assertEqual(tas[i], list_tas[i], msg="All elements in the list should be the same as the db.")

    pass


class Test_Get_All_Instructors(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
            Creates a db with 50 users, 10 courses and 20 labs.
            All randomly linked in legal (and logical) ways.
            """
        for i in range(0, 50):
            UserFactory(password="shjsfahjk")

        for i in range(0, 10):
            CourseFactory()

    def test_actually_returns_valid(self):
        self.assertIsInstance(user.get_all_instructors(), list,
                              msg=f"Get all should return list, returned {type(user.get_all_instructors())}")

    def test_count_correct(self):
        instructors = models.User.objects.filter(groups__name="Instructor")

        list_instructors: list = user.get_all_instructors()

        self.assertIsNotNone(list_instructors, msg="Should return empty list instead!")
        self.assertEqual(len(instructors), len(list_instructors),
                         msg=f"All tas should include all tas in the db. Actual: {len(instructors)} Is {len(list_instructors)}")

    def test_exhaustive(self):
        tas = list(models.User.objects.filter(groups__name="Instructor").all())
        tas = sorted(tas, key=lambda x: x.email)
        list_tas: list = user.get_all_instructors()
        list_tas = sorted(tas, key=lambda x: x.email)

        for i in range(0, min(len(tas), len(list_tas))):
            self.assertEqual(tas[i], list_tas[i], msg="All elements in the list should be the same as the db.")


class Test_Get_All_Admins(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
            Creates a db with 50 users, 10 courses and 20 labs.
            All randomly linked in legal (and logical) ways.
            """
        for i in range(0, 50):
            UserFactory(password="sdfshsd")

        for i in range(0, 10):
            CourseFactory()

    def test_actually_returns_valid(self):
        self.assertIsInstance(user.get_all_admins(), list,
                              msg=f"Get all should return list, returned {type(user.get_all_admins())}")

    def test_count_correct(self):
        admins = models.User.objects.filter(groups__name="Admin")

        list_admins: list = user.get_all_admins()

        self.assertIsNotNone(list_admins, msg="Should return empty list instead!")
        self.assertEqual(len(admins), len(list_admins),
                         msg=f"All tas should include all tas in the db. Actual: {len(admins)} Is {len(list_admins)}")

    def test_exhaustive(self):
        tas = list(models.User.objects.filter(groups__name="Admin").all())
        tas = sorted(tas, key=lambda x: x.email)
        list_tas: list = user.get_all_admins()
        list_tas = sorted(tas, key=lambda x: x.email)

        for i in range(0, min(len(tas), len(list_tas))):
            self.assertEqual(tas[i], list_tas[i], msg="All elements in the list should be the same as the db.")


class Test_Get_Assigned_Tas(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
            Creates a db with 50 users, 10 courses and 20 labs.
            All randomly linked in legal (and logical) ways.
            """
        for i in range(0, 50):
            UserFactory(password="sdfshsd")

        for i in range(0, 10):
            CourseFactory()

    def setUp(self):
        self.InstructorList = user.get_all_instructors()

    def test_actually_returns_valid(self):
        for instructor in self.InstructorList:
            self.assertIsInstance(Instructor(instructor).get_assigned_tas(), list,
                                  msg=f"Get all should return list, returned {type(Instructor(instructor).get_assigned_tas())}")

    def test_only_tas(self):
        for instructor in self.InstructorList:
            for ta in Instructor(instructor).get_assigned_tas():
                self.assertTrue(is_ta(ta),
                                msg='get_assigned_tas returned a list that included a user who was not a ta!')


class Test_Send_Email(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
            Creates a db with 50 users, 10 courses and 20 labs.
            All randomly linked in legal (and logical) ways.
            """
        for i in range(0, 50):
            UserFactory(password="sdfshsd")

        for i in range(0, 10):
            CourseFactory()

    def setUp(self):
        self.InstructorList = user.get_all_instructors()
        self.AdminList = user.get_all_admins()
        self.Header = 'Header'
        self.Body = 'Body'

    def test_actually_returns_valid(self):
        for instructor in self.InstructorList:
            self.assertIsInstance(Instructor(instructor).send_email(self.Header, self.Body), list, msg=f'send_email failed to return a list, returned {type(Instructor(instructor).send_email(self.Header, self.Body))}')
        for admin in self.AdminList:
            self.assertTrue(Admin(admin).send_email(self.Header, self.Body), msg=f'send_email failed to return a list, returned {type(Instructor(instructor).send_email(self.Header, self.Body))}')

    def test_correct_recipients(self):
        for instructor in self.InstructorList:
            recipients = Instructor(instructor).send_email(self.Header, self.Body)
            self.assertEqual(len(Instructor(instructor).get_assigned_tas()), len(recipients), msg='The number of tas an instructor has and the amount that recieved an email did not match')
            for ta in Instructor(instructor).get_assigned_tas():
                self.assertIn(ta.email, recipients, msg='Not all of the correct ta emails were included in the recipients')
        for admin in self.AdminList:
            recipients = Admin(admin).send_email(self.Header, self.Body)
            self.assertEqual(len(user.get_all_users()), len(recipients), msg='The number of users and the amount that recieved an email did not match')
            for single_user in user.get_all_users():
                self.assertIn(single_user.email, recipients, msg='Not all of the correct emails were included in the recipients')
