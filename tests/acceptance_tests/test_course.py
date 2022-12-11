from django.contrib.auth.models import User
from django.test import TestCase, Client
from Factories import *
from TA_Scheduler.user import make_admin, make_instructor, make_ta


class TestCourseCreate(TestCase):
    def setUp(self):
        UserFactory()

        self.Admin = User.objects.create_user('admin1', password='admin1')
        self.Admin.save()
        make_admin(self.Admin.account)

        self.Instructor = User.objects.create_user('instructor1', password='instructor1')
        self.Instructor.save()
        make_instructor(self.Instructor.account)

        self.Ta = User.objects.create_user('ta1', password='ta1')
        self.Ta.save()
        make_ta(self.Ta.account)
        self.wrong_passwords = {'apple', 'banana', 'pear', '12345', 'password123', 'hello', 'goodbye'}

    def test_course_create_default(self):
        client = Client()
        client.login(username='admin1', password='admin1')

        response = client.post(f'/course/create/', {'term_type': 'spr', 'term_year': '2022', 'course_number': '123', 'subject': 'tester', 'name': 'test', 'description': 'test'}, follow=True)
        course_id = response.context['course'].id

        self.assertRedirects(response, f'/course/{course_id}/view/')

    def test_course_create_not_admin(self):
        client = Client()
        client.login(username='ta1', password='ta1')

        response = client.get(f'/course/create/', follow=True)

        self.assertEqual(response.status_code, 403, msg='User wasnt presented with a 403 error when going to the course creation url!')

    def test_course_create_not_logged_in(self):
        client = Client()

        response = client.get(f'/course/create/', follow=True)

        self.assertRedirects(response, f'/accounts/login/')


