from django.core import mail
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, Client
from tests.Factories import *
from TA_Scheduler.models import User, Course
from TA_Scheduler.user import make_admin, make_instructor, make_ta
from phonenumber_field.modelfields import PhoneNumber


class TestLogin(TestCase):
    def setUp(self):
        # Creates a dummy db
        for i in range(0, 10):
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

        self.wrong_passwords = {'apple', 'banana', 'pear', '12345', 'password123', 'hello', 'goodbye'}

    def test_AdminCorrectInfo(self):
        client = Client()
        self.assertTrue(client.login(email=self.Admin.email, password='admin1'), "Successful admin login doesn't "
                                                                                 "return true")
        resp = client.get(f'/accounts/{self.Admin.id}/view/')
        self.assertEqual(resp.status_code, 200, "Get accounts view did not return status code 200 (OK) after "
                                                "successful admin login")

        self.assertTemplateUsed(resp, 'account/view_account.html', "Get accounts view did not return the correct "
                                                                   "template successful admin login")

    def test_AdminWrongPassword(self):
        client = Client()
        for i in self.wrong_passwords:
            self.assertFalse(client.login(email=self.Admin.email, password=i))
            resp = client.get(f'/accounts/{self.Admin.id}/view/')
            self.assertNotEqual(resp.status_code, 200, "Get accounts view returned status code 200 (OK) after "
                                                       "using wrong admin password")

            self.assertTemplateNotUsed(resp, 'account/view_account.html', "Get accounts view returned the successful "
                                                                          "login template after an unsuccessful admin"
                                                                          " login")

    def test_AdminWrongUsername(self):
        client = Client()
        for i in self.wrong_passwords:
            self.assertFalse(client.login(email=i, password="admin1"))
            resp = client.get(f'/accounts/{self.Admin.id}/view/')
            self.assertNotEqual(resp.status_code, 200, "Get accounts view returned status code 200 (OK) after "
                                                       "using wrong admin username")

            self.assertTemplateNotUsed(resp, 'account/view_account.html', "Get accounts view returned the successful "
                                                                          "login template after an unsuccessful admin"
                                                                          " login")

    def test_InstructorCorrectInfo(self):
        client = Client()
        self.assertTrue(client.login(email=self.Instructor.email, password='instructor1'), "Successful "
                                                                                           "instructor login "
                                                                                           "doesn't return true")
        resp = client.get(f'/accounts/{self.Instructor.id}/view/')
        self.assertEqual(resp.status_code, 200, "Get accounts view did not return status code 200 (OK) after "
                                                "successful instructor login")

        self.assertTemplateUsed(resp, 'account/view_account.html', "Get accounts view did not return the correct "
                                                                   "template successful instructor login")

    def test_InstructorWrongPassword(self):
        client = Client()
        for i in self.wrong_passwords:
            self.assertFalse(client.login(email=self.Instructor.email, password=i))
            resp = client.get(f'/accounts/{self.Instructor.id}/view/')
            self.assertNotEqual(resp.status_code, 200, "Get accounts view returned status code 200 (OK) after "
                                                       "using wrong instructor password")

            self.assertTemplateNotUsed(resp, 'account/view_account.html', "Get accounts view returned the successful "
                                                                          "login template after an unsuccessful "
                                                                          "instructor login")

    def test_InstructorWrongUsername(self):
        client = Client()
        for i in self.wrong_passwords:
            self.assertFalse(client.login(email=i, password="instructor1"))
            resp = client.get(f'/accounts/{self.Instructor.id}/view/')
            self.assertNotEqual(resp.status_code, 200, "Get accounts view returned status code 200 (OK) after "
                                                       "using wrong instructor username")

            self.assertTemplateNotUsed(resp, 'account/view_account.html', "Get accounts view returned the successful "
                                                                          "login template after an unsuccessful "
                                                                          "instructor login")

    def test_TaCorrectInfo(self):
        client = Client()
        self.assertTrue(client.login(email=self.TA.email, password='ta1'), "Successful ta login doesn't return "
                                                                           "true")
        resp = client.get(f'/accounts/{self.TA.id}/view/')
        self.assertEqual(resp.status_code, 200, "Get accounts view did not return status code 200 (OK) after "
                                                "successful ta login")

        self.assertTemplateUsed(resp, 'account/view_account.html', "Get accounts view did not return the correct "
                                                                   "template successful ta login")

    def test_TaWrongPassword(self):
        client = Client()
        for i in self.wrong_passwords:
            self.assertFalse(client.login(email=self.TA.email, password=i))
            resp = client.get(f'/accounts/{self.TA.id}/view/')
            self.assertNotEqual(resp.status_code, 200, "Get accounts view returned status code 200 (OK) after "
                                                       "using wrong ta password")

            self.assertTemplateNotUsed(resp, 'account/view_account.html', "Get accounts view returned the successful "
                                                                          "login template after an unsuccessful ta "
                                                                          "login")

    def test_TaWrongUsername(self):
        client = Client()
        for i in self.wrong_passwords:
            self.assertFalse(client.login(email=i, password="ta1"))
            resp = client.get(f'/accounts/{self.Instructor.id}/view/')
            self.assertNotEqual(resp.status_code, 200, "Get accounts view returned status code 200 (OK) after "
                                                       "using wrong ta username")

            self.assertTemplateNotUsed(resp, 'account/view_account.html', "Get accounts view returned the successful "
                                                                          "login template after an unsuccessful ta "
                                                                          "login")


class TestViewPublicContactInfo(TestCase):

    def setUp(self):

        for i in range(0, 10):
            UserFactory()

        self.userList = list(models.User.objects.all())

    def test_logged_in(self):

        for i in self.userList:
            client = Client()
            client.login(email=i.email, password='password')

            for k in self.userList:
                if k != i:
                    resp = client.get(f'/accounts/{k.id}/view/')

                    for x in resp.context:
                        found_phone_num = x['user'].phone_number
                        found_email = x['user'].email

                        self.assertGreaterEqual(len(found_phone_num), 1, "Phone number not found")
                        self.assertIsInstance(found_phone_num, PhoneNumber, "Found phone number is not of type "
                                                                            "PhoneNumber")

                        self.assertGreaterEqual(len(found_email), 1, "Email not found")
                        self.assertIsInstance(found_email, str, "Found email is not of type String")

    def test_not_logged_in(self):

        for i in self.userList:
            client = Client()

            for k in self.userList:
                if k != i:
                    resp = client.get(f'/accounts/{k.id}/view/', follow=True)

                    self.assertRedirects(resp, f'/accounts/login/?next=/accounts/{k.id}/view/', status_code=302,
                                         target_status_code=200, msg_prefix="Attempt to view contact info while not "
                                                                            "logged does not redirect to login screen")


class TestAddressCreation(TestCase):

    def setUp(self):
        UserFactory()
        self.Admin = User.objects.create_user('test1', 'test1', 'test1', password='test1')
        self.Admin.save()
        self.Admin.groups.clear()
        make_admin(self.Admin)
        UserFactory()
        self.ArbitraryUser = User.objects.create_user('test2', 'test2', 'test2', password='test2')

    def test_CreateAddressAdminSelf(self):
        client = Client()
        client.login(username='test1', password='test1')
        view_account = client.get(f'/accounts/{self.Admin.id}/view/')
        self.assertEqual(self.Admin.id, client.session['account_id_to_change'], msg='Session was not saved!')
        create_address = client.post(f'/address/create/',
                                     {'state': 'WI', 'city': 'Milwaukee', 'street_address': 'A very real street',
                                      'zip_code': '53201'}, follow=True)

        self.assertEqual('account/view_account.html', create_address.template_name[0],
                         msg="After address is created user should be redirected to the view of that address.")
        self.assertTrue(User.objects.get(id=self.Admin.id).address.id, msg="Address was not set!")

    def test_CreateAddressForOther(self):
        client = Client()
        client.login(username='test1', password='test1')
        view_account = client.get(f'/accounts/{self.ArbitraryUser.id}/view/')
        self.assertEqual(self.ArbitraryUser.id, client.session['account_id_to_change'],
                         msg='Session was not saved!')
        create_address = client.post(f'/address/create/',
                                     {'state': 'WI', 'city': 'Milwaukee', 'street_address': 'A very real street',
                                      'zip_code': '53201'}, follow=True)

        self.assertEqual('account/view_account.html', create_address.template_name[0],
                         msg="After address is created user should be redirected to the view of that address.")
        self.assertTrue(User.objects.get(id=self.ArbitraryUser.id).address.id, msg="Address was not set!")

    def test_CreateAddressNoContext(self):
        client = Client()
        client.login(username='test1', password='test1')
        create_address = client.post(f'/address/create/',
                                     {'state': 'WI', 'city': 'Milwaukee', 'street_address': 'A very real street',
                                      'zip_code': '53201'}, follow=True)
        self.assertEqual(create_address.status_code, 403, "The user went straight to the create page and we don't "
                                                          "have the context for who's address we should create.")
        pass


class TestUserCreation(TestCase):
    def setUp(self):
        # Creates a dummy db
        for i in range(0, 10):
            UserFactory(password="not_signinable")

        self.Admin = User.objects.create_user(email='admin@admin.com', first_name='admin1', last_name='admin1',
                                              password='admin1')
        self.Admin.groups.clear()
        make_admin(self.Admin)
        self.User = User.objects.create_user(email='user@user.com', first_name='user', last_name='user',
                                             password='user')

    def test_create_user_default(self):
        client = Client()
        client.login(email='admin@admin.com', password='admin1')

        create_account = client.post(f'/accounts/register/',
                                     {'email': 'bigtester@test.com', 'first_name': 'biggest', 'last_name': 'tester',
                                      'password1': 'MegaSuperPassw00rd',
                                      'password2': 'MegaSuperPassw00rd'}, follow=True)

        account = create_account.context['object']
        self.assertEqual('bigtester@test.com', account.email, msg="The user was redirected to the wrong page!")

    def test_create_user_account_already_exists(self):
        client = Client()
        client.login(email='admin@admin.com', password='admin1')

        create_account = client.post(f'/accounts/register/',
                                     {'email': 'user@user.com', 'first_name': 'biggest', 'last_name': 'tester',
                                      'password1': 'MegaSuperPassw00rd',
                                      'password2': 'MegaSuperPassw00rd'}, follow=True)

        error_list = create_account.context['errors']
        self.assertEqual('* User with this Email address already exists.', error_list.as_text(),
                         msg="User wasn't shown the right error when attempting to create an account that already "
                             "exists!")

    def test_create_user_invalid_password_similar(self):
        client = Client()
        client.login(email='admin@admin.com', password='admin1')

        create_account = client.post(f'/accounts/register/',
                                     {'email': 'bigtester@test.com', 'first_name': 'biggest', 'last_name': 'tester',
                                      'password1': 'biggest',
                                      'password2': 'biggest'}, follow=True)
        error_list = []

        # gets all errors present on the page
        for x in create_account.context:
            if 'errors' in x:
                for y in x['errors']:
                    error_list.append(y)

        self.assertIn('The password is too similar to the first name.', error_list,
                      msg="Password too similar to username but error didnt appear!")

    def test_create_user_invalid_password_short(self):
        client = Client()
        client.login(email='admin@admin.com', password='admin1')

        create_account = client.post(f'/accounts/register/',
                                     {'email': 'bigtester@test.com', 'first_name': 'biggest', 'last_name': 'tester',
                                      'password1': 'a',
                                      'password2': 'a'}, follow=True)
        error_list = []

        # gets all errors present on the page
        for x in create_account.context:
            if 'errors' in x:
                for y in x['errors']:
                    error_list.append(y)

        self.assertIn('This password is too short. It must contain at least 8 characters.', error_list,
                      msg="Password too short but error didnt appear!")

    def test_create_user_invalid_password_common(self):
        client = Client()
        client.login(email='admin@admin.com', password='admin1')

        create_account = client.post(f'/accounts/register/',
                                     {'email': 'bigtester@test.com', 'first_name': 'biggest', 'last_name': 'tester',
                                      'password1': 'password',
                                      'password2': 'password'}, follow=True)
        error_list = []

        # gets all errors present on the page
        for x in create_account.context:
            if 'errors' in x:
                for y in x['errors']:
                    error_list.append(y)

        self.assertIn('This password is too common.', error_list, msg="Password too common but error didnt appear!")

    def test_create_user_invalid_password_all_numeric(self):
        client = Client()
        client.login(email='admin@admin.com', password='admin1')

        create_account = client.post(f'/accounts/register/',
                                     {'email': 'bigtester@test.com', 'first_name': 'biggest', 'last_name': 'tester',
                                      'password1': '12',
                                      'password2': '12'}, follow=True)
        error_list = []

        # gets all errors present on the page
        for x in create_account.context:
            if 'errors' in x:
                for y in x['errors']:
                    error_list.append(y)

        self.assertIn('This password is entirely numeric.', error_list,
                      msg="Password was entirely numeric but error didnt appear!")

    def test_create_user_invalid_passwords_dont_match(self):
        client = Client()
        client.login(email='admin@admin.com', password='admin1')

        create_account = client.post(f'/accounts/register/',
                                     {'email': 'bigtester@test.com', 'first_name': 'biggest', 'last_name': 'tester',
                                      'password1': 'biggest',
                                      'password2': 'biggesasast'}, follow=True)
        error_list = []

        # gets all errors present on the page
        for x in create_account.context:
            if 'errors' in x:
                for y in x['errors']:
                    error_list.append(y)

        self.assertIn('The two password fields didn’t match.', error_list,
                      msg="The passwords didnt match but error didnt appear!")

    def test_create_user_not_admin(self):
        client = Client()
        client.login(email='user@user.com', password='user')
        create_account = client.get(f'/accounts/register', follow=True)
        self.assertEqual(create_account.status_code, 403,
                         msg="User was not met with a 403 error when not logged in as an admin!")


class TestAccountDeletion(TestCase):
    def setUp(self):
        # Creates a dummy db
        for i in range(0, 10):
            UserFactory(password="not_signinable")

        self.Admin = User.objects.create_user(email='admin1@test.com', first_name='admin1', last_name='admin1',
                                              password='admin1')
        self.Admin.groups.clear()
        make_admin(self.Admin)
        self.ArbitraryUser = User.objects.create_user(email='user1@test.com', first_name='user1', last_name='user1',
                                                      password='user1')

    def test_delete_account_default(self):
        client = Client()
        client.login(email='admin1@test.com', password='admin1')

        resp = client.post(f'/account/{self.ArbitraryUser.id}/delete', follow=True)
        resp.context['view'].form_valid(f'/account/{self.ArbitraryUser.id}/delete/')

        response = client.get(f'/accounts/{self.ArbitraryUser.id}/view', follow=True)
        self.assertEqual(response.status_code, 404, msg="Deleted user's account page still exists!")
        self.assertEqual(response.context['exception'], 'No user found matching the query',
                         msg='No user found wasnt the cause fo the 404!')

    def test_delete_account_not_logged_in(self):
        client = Client()
        resp = client.get(f'/account/{self.Admin.id}/delete', follow=True)
        self.assertRedirects(resp, f'/accounts/login/?next=/account/{self.Admin.id}/delete/', status_code=301,
                             target_status_code=200)

    def test_delete_account_not_admin(self):
        client = Client()
        client.login(email='user1@test.com', password='user1')

        response = client.get(f'/account/{self.Admin.id}/delete', follow=True)
        self.assertEqual(response.status_code, 403, msg="A user that wasnt an admin was able to view an account "
                                                        "delete page!")

    def test_delete_account_cancel(self):
        client = Client()
        client.login(email='admin1@test.com', password='admin1')

        client.post(f'/account/{self.ArbitraryUser.id}/delete', follow=True)
        response = client.get(f'/accounts/{self.ArbitraryUser.id}/view/')

        self.assertNotEqual(response.status_code, 404, "User was deleted even though the operation was canceled!")
        self.assertEqual(response.context['object'].id, self.ArbitraryUser.id,
                         msg='The user did not match the user on the page!')


class TestEditAccountNoUser(TestCase):
    def setUp(self):
        # Creates a dummy db
        for i in range(0, 10):
            UserFactory(password="not_signinable")

        self.ArbitraryUser = UserFactory.create()

    def test_edit_account_info_not_logged_in(self):
        client = Client()
        response = client.get(f'/accounts/{self.ArbitraryUser.id}/update/', follow=True)
        self.assertRedirects(response, f'/accounts/login/?next=/accounts/{self.ArbitraryUser.id}/update/')

    def test_edit_account_info_user_doesnt_exist_not_admin(self):
        client = Client()
        response = client.get(f'/accounts/12345667/update/', follow=True)
        self.assertRedirects(response, f'/accounts/login/?next=/accounts/12345667/update/')


class TestEditOwnAccountAsAdmin(TestCase):
    def setUp(self):
        # Creates a dummy db
        for i in range(0, 10):
            UserFactory(password="not_signinable")

        self.Admin = User.objects.create_user(email='admin1@test.com', first_name='admin1', last_name='admin1',
                                              password='admin1')
        self.Admin.groups.clear()
        make_admin(self.Admin)

    def test_edit_own_info_as_admin(self):
        client = Client()
        client.login(email='admin1@test.com', password='admin1')

        response = client.post(f'/accounts/{self.Admin.id}/update/',
                               {'first_name': 'test1', 'last_name': 'test1', 'email': 'admin1@test.com',
                                'phone_number': '+12624242825'}, follow=True)

        account_id = response.context['object'].id

        self.assertEqual(self.Admin.id, account_id,
                         msg="User was not redirected to their account page after editing their info!")


class TestEditOtherAccountAsAdmin(TestCase):

    def setUp(self):
        # Creates a dummy db
        for i in range(0, 10):
            UserFactory(password="not_signinable")

        self.Admin = User.objects.create_user(email='admin1@test.com', first_name='admin1', last_name='admin1',
                                              password='admin1')
        self.Admin.groups.clear()
        make_admin(self.Admin)
        self.ArbitraryUser = User.objects.create_user(email='user1@test.com', first_name='user1', last_name='user1',
                                                      password='user1')

    def test_edit_other_account_info_as_admin(self):
        client = Client()
        client.login(email='admin1@test.com', password='admin1')

        response = client.post(f'/accounts/{self.ArbitraryUser.id}/update/',
                               {'first_name': 'test1', 'last_name': 'test1', 'email': 'test@test.com',
                                'phone_number': '+12624242825'}, follow=True)

        account_id = response.context['object'].id

        self.assertEqual(self.ArbitraryUser.id, account_id,
                         msg="User was not redirected to the account page they changed after editing its info!")

    def test_edit_account_info_user_doesnt_exist_admin(self):
        client = Client()
        client.force_login(self.Admin)
        with self.assertRaises(ObjectDoesNotExist, msg="DoesNotExist error not thrown when going to an account page that doesnt exist!"):
            client.post(f'/accounts/123456/update/', follow=True)


class TestEditAccountAsInstructor(TestCase):

    def setUp(self):
        # Creates a dummy db
        for i in range(0, 10):
            UserFactory(password="not_signinable")

        self.Instructor = User.objects.create_user(email='instructor1@test.com', first_name='instructor1',
                                                   last_name='instructor1', password='instructor1')
        self.Instructor.groups.clear()
        make_instructor(self.Instructor)
        self.ArbitraryUser = User.objects.create_user(email='user1@test.com', first_name='user1', last_name='user1'
                                                      , password='user1')

    def test_edit_own_account_info_as_instructor(self):
        client = Client()
        client.login(email='instructor1@test.com', password='instructor1')

        response = client.post(f'/accounts/{self.Instructor.id}/update/',
                               {'first_name': 'test1', 'last_name': 'test1', 'email': 'test@test.com',
                                'phone_number': '+12624242825'}, follow=True)

        account_id = response.context['object'].id

        self.assertEqual(self.Instructor.id, account_id,
                         msg="User was not redirected to their account page after they changed its info!")

    def test_edit_other_account_as_instructor(self):
        client = Client()
        client.login(email='instructor1@test.com', password='instructor1')

        response = client.post(f'/accounts/{self.ArbitraryUser.id}/update/',
                               {'first_name': 'test1', 'last_name': 'test1', 'email': 'test@test.com',
                                'phone_number': '+12624242825'}, follow=True)

        self.assertEqual(response.status_code, 403, msg="User wasnt forbidden from changing another users info!")


class TestEditAccountAsTA(TestCase):

    def setUp(self):
        # Creates a dummy db
        for i in range(0, 10):
            UserFactory(password="not_signinable")

        self.TA = User.objects.create_user(email='ta1@test.com', first_name='ta1', last_name='ta1', password='ta1')
        self.TA.groups.clear()
        make_ta(self.TA)
        self.ArbitraryUser = User.objects.create_user(email='user1@test.com', first_name='user1', last_name='user1',
                                                      password='user1')

    def test_edit_own_account_info_as_ta(self):
        client = Client()
        client.login(email='ta1@test.com', password='ta1')

        response = client.post(f'/accounts/{self.TA.id}/update/',
                               {'first_name': 'test1', 'last_name': 'test1', 'email': 'test@test.com',
                                'phone_number': '+12624242825'}, follow=True)

        account_id = response.context['object'].id

        self.assertEqual(self.TA.id, account_id,
                         msg="User was not redirected to their account page after they changed its info!")

    def test_edit_other_account_as_ta(self):
        client = Client()
        client.login(email='ta1@test.com', password='ta1')

        response = client.post(f'/accounts/{self.ArbitraryUser.id}/update/',
                               {'first_name': 'test1', 'last_name': 'test1', 'email': 'test@test.com',
                                'phone_number': '+12624242825'}, follow=True)

        self.assertEqual(response.status_code, 403, msg="User wasnt forbidden from changing another users info!")


class TestNotify(TestCase):

    def setUp(self):
        self.Header = 'tester'
        self.Body = 'biggest tester alive!'

        self.Admin = UserFactory.create()
        self.Admin.groups.clear()
        make_admin(self.Admin)

        self.Instructor = UserFactory.create()
        self.Instructor.groups.clear()
        make_instructor(self.Instructor)

        self.TA = UserFactory.create()
        self.TA.groups.clear()
        make_ta(self.TA)

        self.myCourse = Course.objects.create()
        self.myCourse.assigned_people.add(self.TA, self.Instructor)

    def test_notify_as_admin(self):
        client = Client()
        client.force_login(self.Admin)
        response = client.post(f'/announcement/', {'header': self.Header, 'content': self.Body},
                               follow=True)
        self.assertEqual(len(mail.outbox), 1, msg='Outbox size wasnt 1!')
        self.assertEqual(mail.outbox[0].subject, self.Header, msg='The subject of the email was wrong')
        self.assertEqual(mail.outbox[0].body, self.Body, msg='The body of the email was wrong')
        self.assertRedirects(response, f'/home/admin/')

    def test_notify_as_instructor(self):
        client = Client()
        client.force_login(self.Instructor)
        response = client.post(f'/announcement/', {'header': self.Header, 'content': self.Body},
                               follow=True)
        self.assertEqual(len(mail.outbox), 1, msg='Outbox size wasnt 1!')
        self.assertEqual(mail.outbox[0].subject, self.Header, msg='The subject of the email was wrong')
        self.assertEqual(mail.outbox[0].body, self.Body, msg='The body of the email was wrong')
        self.assertRedirects(response, f'/home/instructor/')

    def test_notify_as_ta(self):
        client = Client()
        client.force_login(self.TA)
        response = client.get(f'/announcement/', follow=True)
        self.assertEqual(response.status_code, 403,
                         msg='TA wasnt met with a 403 status code when trying to access the announcements page!')

    def test_notify_not_logged_in(self):
        client = Client()
        response = client.get(f'/announcement/', follow=True)
        self.assertRedirects(response, f'/accounts/login/?next=/announcement/')
