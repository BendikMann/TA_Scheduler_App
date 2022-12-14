from django.test import TestCase, Client
from tests.Factories import *
from TA_Scheduler.models import User
from TA_Scheduler.user import make_admin, make_instructor, make_ta


class TestCourseCreate(TestCase):
    def setUp(self):
        UserFactory()

        self.Admin = User.objects.create_user(email='admin1@test.com', first_name='admin1', last_name='admin1', password='admin1')
        self.Admin.groups.clear()
        make_admin(self.Admin)

        self.Instructor = User.objects.create_user(email='instructor1@test.com', first_name='instructor1', last_name='instructor1', password='instructor1')
        self.Instructor.groups.clear()
        make_instructor(self.Instructor)

        self.TA = User.objects.create_user(email='ta1@test.com', first_name='ta1', last_name='ta1', password='ta1')
        self.TA.groups.clear()
        make_ta(self.TA)

    def test_course_create_default(self):
        client = Client()
        client.login(email='admin1@test.com', password='admin1')

        response = client.post(f'/course/create/', {'term_type': 'spr', 'term_year': '2022', 'course_number': '123', 'subject': 'tester', 'name': 'test', 'description': 'test'}, follow=True)
        course_id = response.context['course'].id

        self.assertRedirects(response, f'/course/{course_id}/view/')

    def test_course_create_not_admin(self):
        client = Client()
        client.login(email='ta1@test.com', password='ta1')

        response = client.get(f'/course/create/', follow=True)

        self.assertEqual(response.status_code, 403, msg='User wasnt presented with a 403 error when going to the course creation url!')

    def test_course_create_not_logged_in(self):
        client = Client()

        response = client.get(f'/course/create/', follow=True)

        self.assertRedirects(response, f'/accounts/login/')
