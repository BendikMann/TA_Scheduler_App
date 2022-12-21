from django.test import TestCase, Client
from tests.Factories import *
from TA_Scheduler.models import User, Course
from TA_Scheduler.model_choice_data import CourseChoices, SectionChoices
from TA_Scheduler.user import make_admin, make_instructor, make_ta, is_instructor, is_ta



class TestCourseCreate(TestCase):
    def setUp(self):
        UserFactory()

        self.Admin = User.objects.create_user(email='admin1@test.com', first_name='admin1', last_name='admin1',
                                              password='admin1')
        self.Admin.groups.clear()
        make_admin(self.Admin)

        self.Instructor = User.objects.create_user(email='instructor1@test.com', first_name='instructor1',
                                                   last_name='instructor1', password='instructor1')
        self.Instructor.groups.clear()
        make_instructor(self.Instructor)

        self.TA = User.objects.create_user(email='ta1@test.com', first_name='ta1', last_name='ta1', password='ta1')
        self.TA.groups.clear()
        make_ta(self.TA)

    def test_course_create_default(self):
        client = Client()
        client.force_login(self.Admin)


        response = client.post(f'/course/create/',
                               {'assigned_people': self.Instructor.id, 'term_type': 'spr', 'term_year': '2022',
                                'course_number': '123', 'subject': 'tester',
                                'name': 'test', 'description': 'test'}, follow=True)
        course_id = response.context['course'].id

        self.assertRedirects(response, f'/course/{course_id}/view/')

    def test_course_create_not_admin(self):
        client = Client()
        client.login(email='ta1@test.com', password='ta1')

        response = client.get(f'/course/create/', follow=True)

        self.assertEqual(response.status_code, 403,
                         msg='User wasnt presented with a 403 error when going to the course creation url!')

    def test_course_create_not_logged_in(self):
        client = Client()

        response = client.get(f'/course/create/', follow=True)

        self.assertRedirects(response, f'/accounts/login/?next=/course/create/')


class TestAssignToCourse(TestCase):
    def setUp(self):
        self.Admin = User.objects.create_user(email='admin@admin.com', first_name='adminFirst', last_name='adminLast',
                                              password='password')
        self.Admin.groups.clear()
        make_admin(self.Admin)

        self.Instructor = User.objects.create_user(email='instructor@instructor.com', first_name='instFirst',
                                                   last_name='instLast', password='password')
        self.Instructor.groups.clear()
        make_instructor(self.Instructor)

        self.Ta = User.objects.create_user(email='ta@ta.com', first_name='taFirst', last_name='taLast',
                                           password='password')
        self.Ta.groups.clear()
        make_ta(self.Ta)

        self.Course = Course.objects.create(term_type=CourseChoices.FALL, term_year=CourseChoices.YEAR2022,
                                            course_number="361", subject="COMPSCI", name="Intro to Software Eng",
                                            description="desc")

    def test_admin_assign_instructor(self):
        client = Client()
        client.login(email='admin@admin.com', password='password')

        resp = client.post(f'/course/{self.Course.id}/update/', {'assigned_people': self.Instructor.id,
                                                                 'term_type': self.Course.term_type,
                                                                 'term_year': self.Course.term_year,
                                                                 'course_number': self.Course.course_number,
                                                                 'subject': self.Course.subject,
                                                                 'name': self.Course.name,
                                                                 'description': self.Course.description}, follow=True)

        self.assertRedirects(resp, f'/course/{self.Course.id}/view/', status_code=302,
                             target_status_code=200, msg_prefix="Attempt to assign instructor to course as admin "
                                                                "does not redirect to course view page on submission")

        self.assertEqual(self.Course.assigned_people.first(), self.Instructor, "Assigned instructor not found in "
                                                                               "assigned people queryset")

    def test_admin_assign_ta(self):
        client = Client()
        client.login(email='admin@admin.com', password='password')

        resp = client.post(f'/course/{self.Course.id}/update/', {'assigned_people': self.Ta.id,
                                                                 'term_type': self.Course.term_type,
                                                                 'term_year': self.Course.term_year,
                                                                 'course_number': self.Course.course_number,
                                                                 'subject': self.Course.subject,
                                                                 'name': self.Course.name,
                                                                 'description': self.Course.description}, follow=True)

        self.assertRedirects(resp, f'/course/{self.Course.id}/view/', status_code=302,
                             target_status_code=200, msg_prefix="Attempt to assign instructor to course as admin "
                                                                "does not redirect to course view page on submission")

        self.assertEqual(self.Course.assigned_people.first(), self.Ta, "Assigned TA not found in assigned people "
                                                                       "queryset")

    def test_admin_assign_multiple(self):
        client = Client()
        client.login(email='admin@admin.com', password='password')

        resp = client.post(f'/course/{self.Course.id}/update/', {'assigned_people': [self.Instructor.id, self.Ta.id],
                                                                 'term_type': self.Course.term_type,
                                                                 'term_year': self.Course.term_year,
                                                                 'course_number': self.Course.course_number,
                                                                 'subject': self.Course.subject,
                                                                 'name': self.Course.name,
                                                                 'description': self.Course.description}, follow=True)

        self.assertRedirects(resp, f'/course/{self.Course.id}/view/', status_code=302,
                             target_status_code=200, msg_prefix="Attempt to assign instructor and TA to course as "
                                                                "admin does not redirect to course view page on "
                                                                "submission")

        assigned_people_set = self.Course.assigned_people.all()

        self.assertEqual(assigned_people_set[0], self.Instructor, "Assigned Instructor not found in "
                                                                  "assigned people queryset")
        self.assertEqual(assigned_people_set[1], self.Ta, "Assigned TA not found in assigned people "
                                                          "queryset")

    def test_not_logged_in(self):
        client = Client()

        resp = client.post(f'/course/{self.Course.id}/update/', {'assigned_people': self.Instructor.id,
                                                                 'term_type': self.Course.term_type,
                                                                 'term_year': self.Course.term_year,
                                                                 'course_number': self.Course.course_number,
                                                                 'subject': self.Course.subject,
                                                                 'name': self.Course.name,
                                                                 'description': self.Course.description}, follow=True)

        self.assertRedirects(resp, f'/accounts/login/?next=/course/{self.Course.id}/update/', status_code=302,
                             target_status_code=200, msg_prefix="Attempt to assign instructor to course while not "
                                                                "logged does not redirect to login screen")

    def test_assign_as_instructor(self):
        client = Client()
        client.login(email='instructor@instructor.com', password='password')

        resp = client.post(f'/course/{self.Course.id}/update/', {'assigned_people': self.Ta.id,
                                                                 'term_type': self.Course.term_type,
                                                                 'term_year': self.Course.term_year,
                                                                 'course_number': self.Course.course_number,
                                                                 'subject': self.Course.subject,
                                                                 'name': self.Course.name,
                                                                 'description': self.Course.description}, follow=True)

        self.assertEqual(resp.status_code, 403, "Attempt to assign TA to course as an Instructor did not result in 403 "
                                                "Forbidden error")

    def test_assign_as_ta(self):
        client = Client()
        client.login(email='ta@ta.com', password='password')

        resp = client.post(f'/course/{self.Course.id}/update/', {'assigned_people': self.Instructor.id,
                                                                 'term_type': self.Course.term_type,
                                                                 'term_year': self.Course.term_year,
                                                                 'course_number': self.Course.course_number,
                                                                 'subject': self.Course.subject,
                                                                 'name': self.Course.name,
                                                                 'description': self.Course.description}, follow=True)

        self.assertEqual(resp.status_code, 403, "Attempt to assign Instructor to course as a TA did not result in 403 "
                                                "Forbidden error")
