from django.test import TestCase
from TA_Scheduler.models import Account
from TA_Scheduler import account_util
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
        cls.admin_account: Account = Factories.UserFactory.create().account
        cls.admin_account.user.groups.clear()
        cls.admin_account.user.groups.add(Group.objects.get(name="Admin"))

        # make a ta account
        cls.ta_account: Account = Factories.UserFactory.create().account
        cls.ta_account.user.groups.clear()
        cls.ta_account.user.groups.add(Group.objects.get(name="TA"))

        # make a instructor account.
        cls.instructor_account: Account = Factories.UserFactory.create().account
        cls.instructor_account.user.groups.clear()
        cls.instructor_account.user.groups.add(Group.objects.get(name="Instructor"))

        cls.admin_instructor_account: Account = Factories.UserFactory.create().account
        cls.admin_instructor_account.user.groups.clear()
        cls.admin_instructor_account.user.groups.add(Group.objects.get(name="Instructor"))
        cls.admin_instructor_account.user.groups.add(Group.objects.get(name="Admin"))

        # make a none account.
        cls.account: Account = Factories.UserFactory.create().account
        cls.account.user.groups.clear()

    def test_type(self):
        self.assertIsInstance(account_util.is_admin(self.admin_account), bool, 'is_admin should always return a bool.')

    def test_not_admin_no_perm(self):
        self.assertEqual(False, account_util.is_admin(self.account),
                         "This account is not an admin, but is admin said it was.")

    def test_not_admin_but_other(self):
        self.assertEqual(False, account_util.is_admin(self.ta_account),
                         "This account is not an admin, but is admin said it was.")

    def test_admin(self):
        self.assertEqual(True, account_util.is_admin(self.admin_account),
                         "This account is an admin, but is admin said it was not.")

    def test_admin_and_instructor(self):
        self.assertEqual(True, account_util.is_admin(self.admin_instructor_account),
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
        cls.admin_account: Account = Factories.UserFactory.create().account
        cls.admin_account.user.groups.clear()
        cls.admin_account.user.groups.add(Group.objects.get(name="Admin"))

        # make a ta account
        cls.ta_account: Account = Factories.UserFactory.create().account
        cls.ta_account.user.groups.clear()
        cls.ta_account.user.groups.add(Group.objects.get(name="TA"))

        # make a instructor account.
        cls.instructor_account: Account = Factories.UserFactory.create().account
        cls.instructor_account.user.groups.clear()
        cls.instructor_account.user.groups.add(Group.objects.get(name="Instructor"))

        cls.admin_instructor_account: Account = Factories.UserFactory.create().account
        cls.admin_instructor_account.user.groups.clear()
        cls.admin_instructor_account.user.groups.add(Group.objects.get(name="Instructor"))
        cls.admin_instructor_account.user.groups.add(Group.objects.get(name="Admin"))

        # make a none account.
        cls.account: Account = Factories.UserFactory.create().account
        cls.account.user.groups.clear()

    def test_type(self):
        self.assertIsInstance(account_util.is_ta(self.admin_account), bool, 'is_ta should always return a bool.')

    def test_not_ta_no_perm(self):
        self.assertEqual(False, account_util.is_ta(self.account),
                         "This account is not a ta, but is ta said it was.")

    def test_not_ta_but_other(self):
        self.assertEqual(False, account_util.is_ta(self.instructor_account),
                         "This account is not a ta, but is ta said it was.")

    def test_is_ta(self):
        self.assertEqual(True, account_util.is_ta(self.ta_account),
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
        cls.admin_account: Account = Factories.UserFactory.create().account
        cls.admin_account.user.groups.clear()
        cls.admin_account.user.groups.add(Group.objects.get(name="Admin"))

        # make a ta account
        cls.ta_account: Account = Factories.UserFactory.create().account
        cls.ta_account.user.groups.clear()
        cls.ta_account.user.groups.add(Group.objects.get(name="TA"))

        # make a instructor account.
        cls.instructor_account: Account = Factories.UserFactory.create().account
        cls.instructor_account.user.groups.clear()
        cls.instructor_account.user.groups.add(Group.objects.get(name="Instructor"))

        cls.admin_instructor_account: Account = Factories.UserFactory.create().account
        cls.admin_instructor_account.user.groups.clear()
        cls.admin_instructor_account.user.groups.add(Group.objects.get(name="Instructor"))
        cls.admin_instructor_account.user.groups.add(Group.objects.get(name="Admin"))

        # make a none account.
        cls.account: Account = Factories.UserFactory.create().account
        cls.account.user.groups.clear()

    def test_type(self):
        self.assertIsInstance(account_util.is_instructor(self.instructor_account), bool, 'is_admin should always return a bool.')

    def test_not_instructor_no_perm(self):
        self.assertEqual(False, account_util.is_instructor(self.account),
                         "This account is not an instructor, but is instructor said it was.")

    def test_not_instructor_but_other(self):
        self.assertEqual(False, account_util.is_instructor(self.ta_account),
                         "This account is not an instructor, but is instructor said it was.")

    def test_instructor(self):
        self.assertEqual(True, account_util.is_instructor(self.instructor_account),
                         "This account is an instructor, but is instructor said it was not.")

    def test_admin_and_instructor(self):
        self.assertEqual(True, account_util.is_instructor(self.admin_instructor_account),
                         "This account is an instructor, but is instructor said it was not.")


class Test_make_admin(TestCase):

    def setUp(self):  # setUp is used here because we will be changing this data.

        # make a admin account
        self.admin_account: Account = Factories.UserFactory.create().account
        self.admin_account.user.groups.clear()
        self.admin_account.user.groups.add(Group.objects.get(name="Admin"))

        # make a ta account
        self.ta_account: Account = Factories.UserFactory.create().account
        self.ta_account.user.groups.clear()
        self.ta_account.user.groups.add(Group.objects.get(name="TA"))

        # make a instructor account.
        self.instructor_account: Account = Factories.UserFactory.create().account
        self.instructor_account.user.groups.clear()
        self.instructor_account.user.groups.add(Group.objects.get(name="Instructor"))

        self.admin_instructor_account: Account = Factories.UserFactory.create().account
        self.admin_instructor_account.user.groups.clear()
        self.admin_instructor_account.user.groups.add(Group.objects.get(name="Instructor"))
        self.admin_instructor_account.user.groups.add(Group.objects.get(name="Admin"))

        self.admin_ta_account: Account = Factories.UserFactory.create().account
        self.admin_ta_account.user.groups.clear()
        self.admin_ta_account.user.groups.add(Group.objects.get(name="TA"))
        self.admin_ta_account.user.groups.add(Group.objects.get(name="Admin"))

        # make a none account.
        self.account: Account = Factories.UserFactory.create().account
        self.account.user.groups.clear()

    def test_on_none_input(self):
        with self.assertRaises(ValueError, msg="None type should raise a value error!"):
            account_util.make_admin(None)

    def test_on_user_input(self):
        with self.assertRaises(ValueError, msg="User type should raise a value error! We want to accept only accounts!"):
            account_util.make_admin(self.account)

    def arbitrary_positive(self, account: Account):
        self.assertTrue(account_util.make_admin(account),
                        msg="This account should have been made admin and make admin returned true.")
        self.assertEqual(Group.objects.get(name="Admin"), account.user.groups.get(name="Admin"),
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
        pass




