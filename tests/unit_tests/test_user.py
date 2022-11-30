from unittest import TestCase
from TA_Scheduler.models import Account
from TA_Scheduler.user import Admin, Instructor, Ta

class TestAdmin(TestCase):

    def TestAdminInit(self):
        test_acct = Account
        pass

    def TestAdminInitWrongType(self):
        test_string = "hello"
        test_int = 1

        with self.assertRaises(ValueError, msg="ValueError not raised when passing Admin a string"):
            a = Admin(test_string)

        with self.assertRaises(ValueError, msg="ValueError not raised when passing Admin an integer"):
            a = Admin(test_int)

    def TestAdminInitWrongAccountType(self):
        pass


class TestInstructor(TestCase):

    def TestInstructorInit(self):
        pass

    def TestInstructorInitWrongType(self):
        test_string = "hello"
        test_int = 1

        with self.assertRaises(ValueError, msg="ValueError not raised when passing Instructor a string"):
            a = Instructor(test_string)

        with self.assertRaises(ValueError, msg="ValueError not raised when passing Instructor an integer"):
            a = Instructor(test_int)

    def TestInstructorInitWrongAccountType(self):
        pass


class TestTa(TestCase):

    def TestTaInit(self):
        pass

    def TestTaInitWrongType(self):
        test_string = "hello"
        test_int = 1

        with self.assertRaises(ValueError, msg="ValueError not raised when passing Ta a string"):
            a = Ta(test_string)

        with self.assertRaises(ValueError, msg="ValueError not raised when passing Ta an integer"):
            a = Ta(test_int)

    def TestTaInitWrongAccountType(self):
        pass
