from django.contrib.auth.models import Group
from django.test import TestCase

import Factories
from Factories import *


class TestFactories(TestCase):
    def test_address_factory(self):
        Factories.UsAddressFactory.create()
        self.assertEqual(1, len(models.UsAddress.objects.all()), msg="UsAddress Factory should create an Address")
        print(models.UsAddress.objects.first())

    def test_user_factory(self):
        Factories.UserFactory.create()
        print(models.Account.objects.first())
        self.assertEqual(1, len(models.Account.objects.all()), msg="User Factory should create an account")

    def test_course_factory(self):
        Factories.CourseFactory.create()
        print(models.Course.objects.first())
        self.assertEqual(1, len(models.Course.objects.all()), msg="Course Factory should create a Course")

    def test_course_factory_with_instructors(self):
        for i in range(0, 100):
            Factories.UserFactory(password="rand")  # perf optimization to not make password.
        Factories.CourseFactory.create()
        Factories.CourseFactory.create()
        Factories.CourseFactory.create()
        self.assertEqual(100, len(models.Account.objects.all()))
        self.assertEqual(3, len(models.Course.objects.all()))
        print(models.Course.objects.all())  # Look here to see if data was linked, it's hard to test.


    def test_lab_factory(self):
        Factories.LabFactory.create()
        self.assertEqual(1, len(models.Lab.objects.all()))
        print(models.Course.objects.all())

    def test_labs_factory_with_instructors_courses(self):
        for i in range(0, 100):
            Factories.UserFactory(password="rand")  # Note: For performance reasons, we omit the hashing process for
                                                    # passwords because these accounts do not need to be signinable

        for i in range(0, 20):
            Factories.CourseFactory()

        for i in range(0, 40):
            Factories.LabFactory()

        self.assertEqual(100, len(models.Account.objects.all()))
        self.assertEqual(20, len(models.Course.objects.all()))
        self.assertEqual(40, len(models.Lab.objects.all()))

        print(models.Account.objects.all())
        print(models.Course.objects.all())
        print(models.Lab.objects.all())
        pass
