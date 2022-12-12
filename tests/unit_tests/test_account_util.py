from django.test import TestCase

import TA_Scheduler.user
from TA_Scheduler.models import UsAddress
from TA_Scheduler.user import *
from django.contrib.auth.models import Group
import Factories


class Test_is_admin(TestCase):
    account = None
    instructor_account = None
    ta_account = None
    admin_account = None
    admin_instructor_account = None

    @classmethod
    def setUpTestData(cls):
        # make a admin account
        cls.admin_account: User = Factories.UserFactory.create()
        cls.admin_account.groups.clear()
        cls.admin_account.groups.add(Group.objects.get(name="Admin"))

        # make a ta account
        cls.ta_account: User = Factories.UserFactory.create()
        cls.ta_account.groups.clear()
        cls.ta_account.groups.add(Group.objects.get(name="TA"))

        # make a instructor account.
        cls.instructor_account: User = Factories.UserFactory.create()
        cls.instructor_account.groups.clear()
        cls.instructor_account.groups.add(Group.objects.get(name="Instructor"))

        cls.admin_instructor_account: User = Factories.UserFactory.create()
        cls.admin_instructor_account.groups.clear()
        cls.admin_instructor_account.groups.add(Group.objects.get(name="Instructor"))
        cls.admin_instructor_account.groups.add(Group.objects.get(name="Admin"))

        # make a none account.
        cls.account: User = Factories.UserFactory.create()
        cls.account.groups.clear()

    def test_type(self):
        self.assertIsInstance(is_admin(self.admin_account), bool, 'is_admin should always return a bool.')

    def test_not_admin_no_perm(self):
        self.assertEqual(False, is_admin(self.account),
                         "This account is not an admin, but is admin said it was.")

    def test_not_admin_but_other(self):
        self.assertEqual(False, is_admin(self.ta_account),
                         "This account is not an admin, but is admin said it was.")

    def test_admin(self):
        self.assertEqual(True, is_admin(self.admin_account),
                         "This account is an admin, but is admin said it was not.")

    def test_admin_and_instructor(self):
        self.assertEqual(True, is_admin(self.admin_instructor_account),
                         "This account is an admin, but is admin said it was not.")


class Test_is_ta(TestCase):
    account = None
    instructor_account = None
    ta_account = None
    admin_account = None
    admin_instructor_account = None

    @classmethod
    def setUpTestData(cls):
        # make a admin account
        cls.admin_account: User = Factories.UserFactory.create()
        cls.admin_account.groups.clear()
        cls.admin_account.groups.add(Group.objects.get(name="Admin"))

        # make a ta account
        cls.ta_account: User = Factories.UserFactory.create()
        cls.ta_account.groups.clear()
        cls.ta_account.groups.add(Group.objects.get(name="TA"))

        # make a instructor account.
        cls.instructor_account: User = Factories.UserFactory.create()
        cls.instructor_account.groups.clear()
        cls.instructor_account.groups.add(Group.objects.get(name="Instructor"))

        cls.admin_instructor_account: User = Factories.UserFactory.create()
        cls.admin_instructor_account.groups.clear()
        cls.admin_instructor_account.groups.add(Group.objects.get(name="Instructor"))
        cls.admin_instructor_account.groups.add(Group.objects.get(name="Admin"))

        # make a none account.
        cls.account: User = Factories.UserFactory.create()
        cls.account.user.groups.clear()

    def test_type(self):
        self.assertIsInstance(is_ta(self.admin_account), bool, 'is_ta should always return a bool.')

    def test_not_ta_no_perm(self):
        self.assertEqual(False, is_ta(self.account),
                         "This account is not a ta, but is ta said it was.")

    def test_not_ta_but_other(self):
        self.assertEqual(False, is_ta(self.instructor_account),
                         "This account is not a ta, but is ta said it was.")

    def test_is_ta(self):
        self.assertEqual(True, is_ta(self.ta_account),
                         "This account is a ta, but is ta said it was not.")


class Test_is_instructor(TestCase):
    account = None
    instructor_account = None
    ta_account = None
    admin_account = None
    admin_instructor_account = None

    @classmethod
    def setUpTestData(cls):
        # make a admin account
        cls.admin_account: User = Factories.UserFactory.create().account
        cls.admin_account.groups.clear()
        cls.admin_account.groups.add(Group.objects.get(name="Admin"))

        # make a ta account
        cls.ta_account: User = Factories.UserFactory.create().account
        cls.ta_account.groups.clear()
        cls.ta_account.groups.add(Group.objects.get(name="TA"))

        # make a instructor account.
        cls.instructor_account: User = Factories.UserFactory.create().account
        cls.instructor_account.groups.clear()
        cls.instructor_account.groups.add(Group.objects.get(name="Instructor"))

        cls.admin_instructor_account: User = Factories.UserFactory.create().account
        cls.admin_instructor_account.groups.clear()
        cls.admin_instructor_account.groups.add(Group.objects.get(name="Instructor"))
        cls.admin_instructor_account.groups.add(Group.objects.get(name="Admin"))

        # make a none account.
        cls.account: User = Factories.UserFactory.create().account
        cls.account.user.groups.clear()

    def test_type(self):
        self.assertIsInstance(is_instructor(self.instructor_account), bool,
                              'is_admin should always return a bool.')

    def test_not_instructor_no_perm(self):
        self.assertEqual(False, is_instructor(self.account),
                         "This account is not an instructor, but is instructor said it was.")

    def test_not_instructor_but_other(self):
        self.assertEqual(False, is_instructor(self.ta_account),
                         "This account is not an instructor, but is instructor said it was.")

    def test_instructor(self):
        self.assertEqual(True, is_instructor(self.instructor_account),
                         "This account is an instructor, but is instructor said it was not.")

    def test_admin_and_instructor(self):
        self.assertEqual(True, is_instructor(self.admin_instructor_account),
                         "This account is an instructor, but is instructor said it was not.")


class Test_make_admin(TestCase):

    def setUp(self):  # setUp is used here because we will be changing this data.

        # make a admin account
        self.admin_account: User = Factories.UserFactory.create()
        self.admin_account.groups.clear()
        self.admin_account.groups.add(Group.objects.get(name="Admin"))

        # make a ta account
        self.ta_account: User = Factories.UserFactory.create()
        self.ta_account.groups.clear()
        self.ta_account.groups.add(Group.objects.get(name="TA"))

        # make a instructor account.
        self.instructor_account: User = Factories.UserFactory.create()
        self.instructor_account.groups.clear()
        self.instructor_account.groups.add(Group.objects.get(name="Instructor"))

        self.admin_instructor_account: User = Factories.UserFactory.create()
        self.admin_instructor_account.groups.clear()
        self.admin_instructor_account.groups.add(Group.objects.get(name="Instructor"))
        self.admin_instructor_account.groups.add(Group.objects.get(name="Admin"))

        self.admin_ta_account: User = Factories.UserFactory.create()
        self.admin_ta_account.groups.clear()
        self.admin_ta_account.groups.add(Group.objects.get(name="TA"))
        self.admin_ta_account.groups.add(Group.objects.get(name="Admin"))

        # make a none account.
        self.account: User = Factories.UserFactory.create()
        self.account.groups.clear()

    def test_on_none_input(self):
        with self.assertRaises(TypeError, msg="None type should raise a value error!"):
            make_admin(None)

    def test_on_user_input(self):
        with self.assertRaises(TypeError,
                               msg="User type should raise a value error! We want to accept only accounts!"):
            make_admin(self.account.groups)

    def arbitrary_positive(self, account: User):
        self.assertIsInstance(make_admin(account), TA_Scheduler.user.Admin,
                              msg="This account should have been made admin and make admin returned true.")
        self.assertEqual(Group.objects.get(name="Admin"), account.groups.get(name="Admin"),
                         msg="make admin reported true, but is not in admin group.")

    def test_no_groups(self):
        self.arbitrary_positive(self.account)

    def test_is_instructor(self):
        self.arbitrary_positive(self.instructor_account)

    def test_is_ta(self):
        self.arbitrary_positive(self.ta_account)

    def test_already_admin_ta(self):
        self.arbitrary_positive(self.admin_ta_account)

    def test_already_admin_instructor(self):
        self.arbitrary_positive(self.admin_instructor_account)


class Test_make_ta(TestCase):

    def setUp(self):  # setUp is used here because we will be changing this data.

        # make a admin account
        self.admin_account: User = Factories.UserFactory.create()
        self.admin_account.groups.clear()
        self.admin_account.groups.add(Group.objects.get(name="Admin"))

        # make a ta account
        self.ta_account: User = Factories.UserFactory.create()
        self.ta_account.groups.clear()
        self.ta_account.groups.add(Group.objects.get(name="TA"))

        # make a instructor account.
        self.instructor_account: User = Factories.UserFactory.create()
        self.instructor_account.groups.clear()
        self.instructor_account.groups.add(Group.objects.get(name="Instructor"))

        self.admin_instructor_account: User = Factories.UserFactory.create()
        self.admin_instructor_account.groups.clear()
        self.admin_instructor_account.groups.add(Group.objects.get(name="Instructor"))
        self.admin_instructor_account.groups.add(Group.objects.get(name="Admin"))

        self.admin_ta_account: User = Factories.UserFactory.create()
        self.admin_ta_account.groups.clear()
        self.admin_ta_account.groups.add(Group.objects.get(name="TA"))
        self.admin_ta_account.groups.add(Group.objects.get(name="Admin"))

        # make a none account.
        self.account: User = Factories.UserFactory.create()
        self.account.groups.clear()

    def test_on_none_input(self):
        with self.assertRaises(TypeError, msg="None type should raise a value error!"):
            make_ta(None)

    def test_on_not_user_input(self):
        with self.assertRaises(TypeError,
                               msg="User type should raise a value error! We want to accept only accounts!"):
            make_ta(self.account.groups)

    def arbitrary_positive(self, account: User):
        self.assertIsInstance(make_ta(account), TA_Scheduler.user.Ta,
                              msg="This account should have been made ta and returned a Ta instance.")
        self.assertEqual(Group.objects.get(name="TA"), account.groups.get(name="TA"),
                         msg="make ta reported Ta model, but is not in ta group.")

    def test_account_no_perms(self):
        self.arbitrary_positive(self.account)

    def test_account_admin(self):
        self.arbitrary_positive(self.admin_account)

    def test_account_ta(self):
        self.arbitrary_positive(self.ta_account)

    def test_instructor(self):
        self.assertIsNone(make_ta(self.instructor_account),
                          msg="Instructors cannot add a ta, should return none type.")


class Test_make_instructor(TestCase):
    def setUp(self):  # setUp is used here because we will be changing this data.

        # make a admin account
        self.admin_account: User = Factories.UserFactory.create()
        self.admin_account.groups.clear()
        self.admin_account.groups.add(Group.objects.get(name="Admin"))

        # make a ta account
        self.ta_account: User = Factories.UserFactory.create()
        self.ta_account.groups.clear()
        self.ta_account.groups.add(Group.objects.get(name="TA"))

        # make a instructor account.
        self.instructor_account: User = Factories.UserFactory.create()
        self.instructor_account.groups.clear()
        self.instructor_account.groups.add(Group.objects.get(name="Instructor"))

        self.admin_instructor_account: User = Factories.UserFactory.create()
        self.admin_instructor_account.groups.clear()
        self.admin_instructor_account.groups.add(Group.objects.get(name="Instructor"))
        self.admin_instructor_account.groups.add(Group.objects.get(name="Admin"))

        self.admin_ta_account: User = Factories.UserFactory.create()
        self.admin_ta_account.groups.clear()
        self.admin_ta_account.groups.add(Group.objects.get(name="TA"))
        self.admin_ta_account.groups.add(Group.objects.get(name="Admin"))

        # make a none account.
        self.account: User = Factories.UserFactory.create()
        self.account.groups.clear()

    def test_on_none_input(self):
        with self.assertRaises(TypeError, msg="None type should raise a value error!"):
            make_instructor(None)

    def test_on_user_input(self):
        with self.assertRaises(TypeError,
                               msg="User type should raise a value error! We want to accept only accounts!"):
            make_instructor(self.account)

    def arbitrary_positive(self, account: User):
        self.assertIsInstance(make_instructor(account), TA_Scheduler.user.Instructor,
                              msg="This account should have been made instructor and returned a instructor instance.")
        self.assertEqual(Group.objects.get(name="Instructor"), account.groups.get(name="Instructor"),
                         msg="make instructor returned instructor object, but is not in ta group.")

    def test_already_instructor(self):
        self.arbitrary_positive(self.instructor_account)

    def test_no_groups(self):
        self.arbitrary_positive(self.account)

    def test_ta(self):
        self.assertIsNone(make_instructor(self.ta_account),
                          msg="TA cannot add a instructor group, should return none type.")

