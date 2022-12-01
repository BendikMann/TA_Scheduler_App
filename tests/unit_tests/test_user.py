from django.test import TestCase
from TA_Scheduler import models
from TA_Scheduler.user import Admin
from Factories import *
from TA_Scheduler import user


def init_dummy_database():
    """
    Creates a db with 50 users, 10 courses and 20 labs.
    All randomly linked in legal (and logical) ways.
    """
    for i in range(0, 50):
        UserFactory(password="not_signinable")

    for i in range(0, 10):
        CourseFactory()

    for i in range(0, 20):
        LabFactory()

    pass


class TestInstructor(TestCase):
    pass


class Test_Get_All_Tas(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
            Creates a db with 50 users, 10 courses and 20 labs.
            All randomly linked in legal (and logical) ways.
            """
        for i in range(0, 50):
            UserFactory()

        for i in range(0, 10):
            CourseFactory()

        for i in range(0, 20):
            LabFactory()

    def test_actually_returns_valid(self):
        self.assertIsInstance(user.get_all_tas(), list,
                              msg=f"Get all should return list, returned {type(user.get_all_tas())}")

    def test_count_correct(self):
        tas = models.Account.objects.filter(user__groups__name="Ta")

        list_tas: list[user.Ta] = user.get_all_tas()

        self.assertIsNotNone(list_tas, msg="Should return empty list instead!")
        self.assertEqual(len(tas), len(list_tas),
                         msg=f"All tas should include all tas in the db. Actual: {len(tas)} Is {len(list_tas)}")

    def test_exhaustive(self):
        tas = list(models.Account.objects.filter(user__groups__name="Ta").all())
        tas = sorted(tas, key=lambda x: x.user.username)
        list_tas: list[user.Ta] = user.get_all_tas()
        list_tas = sorted(tas, key=lambda x: x.user.username)

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
            UserFactory()

        for i in range(0, 10):
            CourseFactory()

        for i in range(0, 20):
            LabFactory()

    def test_actually_returns_valid(self):
        self.assertIsInstance(user.get_all_instructors(), list,
                              msg=f"Get all should return list, returned {type(user.get_all_instructors())}")

    def test_count_correct(self):
        tas = models.Account.objects.filter(user__groups__name="Instructor")

        list_tas: list = user.get_all_instructors()

        self.assertIsNotNone(list_tas, msg="Should return empty list instead!")
        self.assertEqual(len(tas), len(list_tas),
                         msg=f"All tas should include all tas in the db. Actual: {len(tas)} Is {len(list_tas)}")

    def test_exhaustive(self):
        tas = list(models.Account.objects.filter(user__groups__name="Instructor").all())
        tas = sorted(tas, key=lambda x: x.user.username)
        list_tas: list = user.get_all_instructors()
        list_tas = sorted(tas, key=lambda x: x.user.username)

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
            UserFactory()

        for i in range(0, 10):
            CourseFactory()

        for i in range(0, 20):
            LabFactory()

    def test_actually_returns_valid(self):
        self.assertIsInstance(user.get_all_admins(), list,
                              msg=f"Get all should return list, returned {type(user.get_all_admins())}")

    def test_count_correct(self):
        tas = models.Account.objects.filter(user__groups__name="Admin")

        list_tas: list = user.get_all_admins()

        self.assertIsNotNone(list_tas, msg="Should return empty list instead!")
        self.assertEqual(len(tas), len(list_tas),
                         msg=f"All tas should include all tas in the db. Actual: {len(tas)} Is {len(list_tas)}")

    def test_exhaustive(self):
        tas = list(models.Account.objects.filter(user__groups__name="Admin").all())
        tas = sorted(tas, key=lambda x: x.user.username)
        list_tas: list = user.get_all_admins()
        list_tas = sorted(list_tas, key=lambda x: x.user.username)

        for i in range(0, min(len(tas), len(list_tas))):
            self.assertEqual(tas[i], list_tas[i], msg="All elements in the list should be the same as the db.")
