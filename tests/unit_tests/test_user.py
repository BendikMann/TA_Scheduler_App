import unittest
from TA_Scheduler.models import Account
from TA_Scheduler.user import Admin, Instructor, Ta


class AdminTests(unittest.TestCase):

    def test_admin_init(self):
        pass

    def test_admin_init_wrong_type(self):
        test_string = "hello"
        test_int = 1

        with self.assertRaises(ValueError, msg="ValueError not raised when passing Admin a string"):
            a = Admin(test_string)

        with self.assertRaises(ValueError, msg="ValueError not raised when passing Admin an integer"):
            a = Admin(test_int)

    def test_admin_init_wrong_account_type(self):
        pass


class InstructorTests(unittest.TestCase):

    def test_instructor_init(self):
        pass

    def test_instructor_init_wrong_type(self):
        test_string = "hello"
        test_int = 1

        with self.assertRaises(ValueError, msg="ValueError not raised when passing Instructor a string"):
            a = Instructor(test_string)

        with self.assertRaises(ValueError, msg="ValueError not raised when passing Instructor an integer"):
            a = Instructor(test_int)

    def test_instructor_init_wrong_account_type(self):
        pass


class TaTests(unittest.TestCase):

    def test_ta_init(self):
        pass

    def test_ta_init_wrong_type(self):
        test_string = "hello"
        test_int = 1

        with self.assertRaises(ValueError, msg="ValueError not raised when passing Ta a string"):
            a = Ta(test_string)

        with self.assertRaises(ValueError, msg="ValueError not raised when passing Ta an integer"):
            a = Ta(test_int)

    def test_ta_init_wrong_account_type(self):
        pass
