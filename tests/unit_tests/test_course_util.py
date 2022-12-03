from django.test import TestCase
from TA_Scheduler.course_util import *
from TA_Scheduler.account_util import *


class TestCourse(TestCase):
    def setUp(self):
        self.teacher = User.objects.create(username="username", first_name="first", last_name="last",
                                           password="password", email="email@emial.com")
        self.course = create_course(self.teacher, "422G", "COMPSCI", "801", "Introduction to Software Engineering")

    def test_create_empty(self):
        with self.assertRaises(TypeError, msg="Incorrect parameters"):
            create_course()

    def test_create_detailed(self):
        a = create_course(self.teacher, "123", "UNIT", "101", "Unit Testing 101")
        self.assertIsNotNone(a)

    def test_create_course_instructor(self):
        self.assertIsNotNone(self.course)
        self.assertEqual(self.course.Instructor, self.teacher, "instructor was not assigned")

    def test_create_course_number(self):
        self.assertIsNotNone(self.course)
        self.assertEqual(self.course.course_number, "422G", "course number was not assigned")

    def test_create_course_section(self):
        self.assertIsNotNone(self.course)
        self.assertEqual(self.course.section, "801", "section number was not assigned")

    def test_create_course_subject(self):
        self.assertIsNotNone(self.course)
        self.assertEqual(self.course.subject, "COMPSCI", "subject was not assigned")

    def test_create_course_name(self):
        self.assertIsNotNone(self.course)
        self.assertEqual(self.course.name, "Introduction to Software Engineering", "course name was not assigned")

    def test_create_course_already_exists(self):
        with self.assertRaises(ValueError, msg="course already exists"):
            create_course(self.teacher, "422G", "COMPSCI", "801", "Introduction to Software Engineering")

