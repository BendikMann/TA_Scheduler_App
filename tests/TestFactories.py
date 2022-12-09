import django.db.utils
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
        print(models.User.objects.first())
        self.assertEqual(1, len(models.User.objects.all()), msg="User Factory should create an account")

    def test_course_factory(self):
        Factories.CourseFactory.create()
        print(models.Course.objects.first())
        self.assertEqual(1, len(models.Course.objects.all()), msg="Course Factory should create a Course")

    def test_course_factory_with_instructors_tas(self):
        for i in range(0, 100):
            Factories.UserFactory(password="rand")  # perf optimization to not make password.
        Factories.CourseFactory.create()
        Factories.CourseFactory.create()
        Factories.CourseFactory.create()
        self.assertEqual(100, len(models.User.objects.all()))
        self.assertEqual(3, len(models.Course.objects.all()))

        # sections should also be created now, but there is a non-zero chance that none are.
        print(models.Course.objects.all())  # Look here to see if data was linked, it's hard to test.

    def test_section_factory(self):
        with self.assertRaises(django.db.utils.IntegrityError, msg="You should not be able to create orphaned instances of section!"):
            Factories.SectionFactory.create()

