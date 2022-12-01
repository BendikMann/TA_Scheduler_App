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

    def test_course_factory_with_instructors(self):
        for i in range(0, 100):
            Factories.UserFactory()
        Factories.CourseFactory.create()
        Factories.CourseFactory.create()
        Factories.CourseFactory.create()
        print(models.Course.objects.all())

    def test_lab_factory(self):
        Factories.LabFactory.create()
        print(models.Course.objects.all())
        pass

    def test_labs_factory_with_instructors_courses(self):
        for i in range(0, 100):
            Factories.UserFactory()

        for i in range(0, 20):
            Factories.CourseFactory()

        for i in range(0, 40):
            Factories.LabFactory()

        print(models.Account.objects.all())
        print(models.Course.objects.all())
        print(models.Lab.objects.all())
        pass
