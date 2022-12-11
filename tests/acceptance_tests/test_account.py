
from TA_Scheduler.models import User
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, Client
from Factories import *
from TA_Scheduler.user import make_admin, make_instructor, make_ta


class TestLogin(TestCase):
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

    def test_AdminCorrectInfo(self):
        client = Client()
        self.assertTrue(client.login(username=self.Admin.username, password='admin1'), "Successful admin login doesn't "
                                                                                       "return true")
        resp = client.get(f'/accounts/{self.Admin.account.id}/view/')
        self.assertEqual(resp.status_code, 200, "Get accounts view did not return status code 200 (OK) after "
                                                "successful admin login")

        self.assertTemplateUsed(resp, 'account/view_account.html', "Get accounts view did not return the correct "
                                                                   "template successful admin login")

    def test_AdminWrongPassword(self):
        client = Client()
        for i in self.wrong_passwords:
            self.assertFalse(client.login(username=self.Admin.username, password=i))
            resp = client.get(f'/accounts/{self.Admin.account.id}/view/')
            self.assertNotEqual(resp.status_code, 200, "Get accounts view returned status code 200 (OK) after "
                                                       "using wrong admin password")

            self.assertTemplateNotUsed(resp, 'account/view_account.html', "Get accounts view returned the successful "
                                                                          "login template after an unsuccessful admin"
                                                                          " login")

    def test_AdminWrongUsername(self):
        client = Client()
        for i in self.wrong_passwords:
            self.assertFalse(client.login(username=i, password="admin1"))
            resp = client.get(f'/accounts/{self.Admin.account.id}/view/')
            self.assertNotEqual(resp.status_code, 200, "Get accounts view returned status code 200 (OK) after "
                                                       "using wrong admin username")

            self.assertTemplateNotUsed(resp, 'account/view_account.html', "Get accounts view returned the successful "
                                                                          "login template after an unsuccessful admin"
                                                                          " login")

    def test_InstructorCorrectInfo(self):
        client = Client()
        self.assertTrue(client.login(username=self.Instructor.username, password='instructor1'), "Successful "
                                                                                                 "instructor login "
                                                                                                 "doesn't return true")
        resp = client.get(f'/accounts/{self.Instructor.account.id}/view/')
        self.assertEqual(resp.status_code, 200, "Get accounts view did not return status code 200 (OK) after "
                                                "successful instructor login")

        self.assertTemplateUsed(resp, 'account/view_account.html', "Get accounts view did not return the correct "
                                                                   "template successful instructor login")

    def test_InstructorWrongPassword(self):
        client = Client()
        for i in self.wrong_passwords:
            self.assertFalse(client.login(username=self.Instructor.username, password=i))
            resp = client.get(f'/accounts/{self.Instructor.account.id}/view/')
            self.assertNotEqual(resp.status_code, 200, "Get accounts view returned status code 200 (OK) after "
                                                       "using wrong instructor password")

            self.assertTemplateNotUsed(resp, 'account/view_account.html', "Get accounts view returned the successful "
                                                                          "login template after an unsuccessful "
                                                                          "instructor login")

    def test_InstructorWrongUsername(self):
        client = Client()
        for i in self.wrong_passwords:
            self.assertFalse(client.login(username=i, password="instructor1"))
            resp = client.get(f'/accounts/{self.Instructor.account.id}/view/')
            self.assertNotEqual(resp.status_code, 200, "Get accounts view returned status code 200 (OK) after "
                                                       "using wrong instructor username")

            self.assertTemplateNotUsed(resp, 'account/view_account.html', "Get accounts view returned the successful "
                                                                          "login template after an unsuccessful "
                                                                          "instructor login")

    def test_TaCorrectInfo(self):
        client = Client()
        self.assertTrue(client.login(username=self.Ta.username, password='ta1'), "Successful ta login doesn't return "
                                                                                 "true")
        resp = client.get(f'/accounts/{self.Ta.account.id}/view/')
        self.assertEqual(resp.status_code, 200, "Get accounts view did not return status code 200 (OK) after "
                                                "successful ta login")

        self.assertTemplateUsed(resp, 'account/view_account.html', "Get accounts view did not return the correct "
                                                                   "template successful ta login")

    def test_TaWrongPassword(self):
        client = Client()
        for i in self.wrong_passwords:
            self.assertFalse(client.login(username=self.Ta.username, password=i))
            resp = client.get(f'/accounts/{self.Ta.account.id}/view/')
            self.assertNotEqual(resp.status_code, 200, "Get accounts view returned status code 200 (OK) after "
                                                       "using wrong ta password")

            self.assertTemplateNotUsed(resp, 'account/view_account.html', "Get accounts view returned the successful "
                                                                          "login template after an unsuccessful ta "
                                                                          "login")

    def test_TaWrongUsername(self):
        client = Client()
        for i in self.wrong_passwords:
            self.assertFalse(client.login(username=i, password="ta1"))
            resp = client.get(f'/accounts/{self.Instructor.account.id}/view/')
            self.assertNotEqual(resp.status_code, 200, "Get accounts view returned status code 200 (OK) after "
                                                       "using wrong ta username")

            self.assertTemplateNotUsed(resp, 'account/view_account.html', "Get accounts view returned the successful "
                                                                          "login template after an unsuccessful ta "
                                                                          "login")

class TestAddressCreation(TestCase):

    def setUp(self):
        UserFactory()
        self.Admin = User.objects.create_user('test1', 'test1', 'test1', password='test1')
        self.Admin.save()
        make_admin(self.Admin)
        UserFactory()
        self.ArbitraryUser = User.objects.create_user('test2', 'test2', 'test2', password='test2')

    def test_CreateAddressAdminSelf(self):
        client = Client()
        client.login(username='test1', password='test1')
        view_account = client.get(f'/accounts/{self.Admin.id}/view/')
        self.assertEqual(self.Admin.id, client.session['account_id_to_change'], msg='Session was not saved!')
        create_address = client.post(f'/address/create/', {'state': 'WI', 'city': 'Milwaukee', 'street_address': 'A very real street', 'zip_code': '53201'}, follow=True)

        self.assertEqual('account/view_account.html', create_address.template_name[0], msg="After address is created user should be redirected to the view of that address.")
        self.assertTrue(User.objects.get(id=self.Admin.id).address.id, msg="Address was not set!")


    def test_CreateAddressForOther(self):
        client = Client()
        client.login(username='test1', password='test1')
        view_account = client.get(f'/accounts/{self.ArbitraryUser.account.id}/view/')
        self.assertEqual(self.ArbitraryUser.account.id, client.session['account_id_to_change'],
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
        UserFactory()
        self.Admin = User.objects.create_user('test1', password='test1')
        self.Admin.save()
        make_admin(self.Admin.account)
        UserFactory()
        self.ArbitraryUser = User.objects.create_user('test2', password='test2')

    def test_create_user_default(self):
        client = Client()
        client.login(username='test1', password='test1')
        create_account = client.post(f'/accounts/register/',
                                     {'username': 'bigtester', 'password1': 'MegaSuperPassw00rd',
                                      'password2': 'MegaSuperPassw00rd'}, follow=True)
        account = create_account.context['object']
        self.assertEqual('bigtester', account.user.username, msg="The user was redirected to the wrong page!")

    def test_create_user_account_already_exists(self):
        client = Client()
        client.login(username='test1', password='test1')
        create_account = client.post(f'/accounts/register/',
                                     {'username': 'test1', 'password1': 'MegaSuperPassw00rd',
                                      'password2': 'MegaSuperPassw00rd'}, follow=True)
        error_list = create_account.context['errors']
        self.assertEqual('* A user with that username already exists.', error_list.as_text(),
                         msg="User wasn't shown the right error when attempting to create an account that already "
                             "exists!")

    def test_create_user_invalid_email(self):
        client = Client()
        client.login(username='test1', password='test1')

    def test_create_user_invalid_password_similar(self):
        client = Client()
        client.login(username='test1', password='test1')
        create_account = client.post(f'/accounts/register/',
                                     {'username': 'test3', 'password1': 'test3',
                                      'password2': 'test3'}, follow=True)
        error_list = []

        # gets all errors present on the page
        for x in create_account.context:
            if 'errors' in x:
                for y in x['errors']:
                    error_list.append(y)

        self.assertIn('The password is too similar to the username.', error_list,
                      msg="Password too similar to username but error didnt appear!")

    def test_create_user_invalid_password_short(self):
        client = Client()
        client.login(username='test1', password='test1')
        create_account = client.post(f'/accounts/register/',
                                     {'username': 'test3', 'password1': 'test3',
                                      'password2': 'test3'}, follow=True)
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
        client.login(username='test1', password='test1')
        create_account = client.post(f'/accounts/register/',
                                     {'username': 'test3', 'password1': 'password',
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
        client.login(username='test1', password='test1')
        create_account = client.post(f'/accounts/register/',
                                     {'username': 'test3', 'password1': '123456',
                                      'password2': '123456'}, follow=True)
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
        client.login(username='test1', password='test1')
        create_account = client.post(f'/accounts/register/',
                                     {'username': 'test3', 'password1': 'test3',
                                      'password2': 'test4'}, follow=True)
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
        client.login(username='test2', password='test2')
        create_account = client.get(f'/accounts/register', follow=True)
        self.assertRedirects(create_account, '/')

    def test_create_user_not_logged_in(self):
        client = Client()
        create_account = client.get(f'/accounts/register', follow=True)
        self.assertRedirects(create_account, '/accounts/login/')


class TestAccountDeletion(TestCase):
    def setUp(self):
        UserFactory()
        self.Admin = User.objects.create_user('test1', password='test1')
        self.Admin.save()
        make_admin(self.Admin.account)
        UserFactory()
        self.ArbitraryUser = User.objects.create_user('test2', password='test2')

    def test_delete_account_default(self):
        # cant hit button
        client = Client()
        client.login(username='test1', password='test1')

        # Create a new user and get its id
        create_account = client.post(f'/accounts/register/',
                                     {'username': 'test4', 'password1': 'MegaSuperPassw00rd',
                                      'password2': 'MegaSuperPassw00rd'}, follow=True)
        account_id = create_account.context['object'].user.id

        resp = client.post(f'/account/{account_id}/delete', follow=True)

        resp.context['view'].form_valid(f'/account/{account_id}/delete/')

        response = client.get(f'/accounts/{account_id}/view', follow=True)
        self.assertEqual(response.status_code, 404, msg="Deleted user's account page still exists!")

    def test_delete_account_not_logged_in(self):
        # attribute error
        client = Client()
        with self.assertRaises(AttributeError, msg="AttributeError not thrown when user is not logged in!"):
            client.get(f'/account/1/delete', follow=True)

    def test_delete_account_not_admin(self):
        client = Client()
        client.login(username='test2', password='test2')
        response = client.get(f'/account/1/delete', follow=True)
        self.assertEqual(response.status_code, 403, msg="A user that wasnt an admin was able to view an account "
                                                        "delete page!")

    def test_delete_account_cancel(self):
        # cant hit button
        client = Client()
        client.login(username='test1', password='test1')

        client.post(f'/account/2/delete', follow=True)
        response = client.get(f'/accounts/2/view/')

        self.assertNotEqual(response.status_code, 404, "User was deleted even though the operation was canceled!")


class TestEditAccountNoUser(TestCase):
    def setUp(self):
        UserFactory()
        self.ArbitraryUser = User.objects.create_user('test2', password='test2')

    def test_edit_account_info_not_logged_in(self):
        client = Client()
        response = client.post(f'/accounts/1/update/', follow=True)
        self.assertRedirects(response, '/accounts/login/')

    def test_edit_account_info_user_doesnt_exist(self):
        client = Client()
        with self.assertRaises(ObjectDoesNotExist, msg="ObjectDoesNotExist error not thrown when going to an account "
                                                       "page that doesnt exist!"):
            client.post(f'/accounts/123456/update/', follow=True)


class TestEditOwnAccountAsAdmin(TestCase):
    def setUp(self):
        self.Admin = User.objects.create_user('test1', password='test1')
        self.Admin.save()
        make_admin(self.Admin.account)

    def test_edit_own_info_as_admin(self):
        client = Client()
        client.login(username='test1', password='test1')

        response = client.post(f'/accounts/1/update/',
                               {'first_name': 'test1', 'last_name': 'test1', 'email': 'test@test.com',
                                'phone_number': '+12624242825'}, follow=True)

        account_id = response.context['object'].user.id

        self.assertEqual(self.Admin.id, account_id,
                         msg="User was not redirected to their account page after editing their info!")


class TestEditOtherAccountAsAdmin(TestCase):

    def setUp(self):
        self.Admin = User.objects.create_user('test1', password='test1')
        self.Admin.save()
        make_admin(self.Admin.account)
        self.ArbitraryUser = User.objects.create_user('test2', password='test2')

    def test_edit_other_account_info_as_admin(self):
        client = Client()
        client.login(username='test1', password='test1')

        response = client.post(f'/accounts/{self.ArbitraryUser.id}/update/',
                               {'first_name': 'test1', 'last_name': 'test1', 'email': 'test@test.com',
                                'phone_number': '+12624242825'}, follow=True)

        account_id = response.context['object'].user.id

        self.assertEqual(self.ArbitraryUser.id, account_id,
                         msg="User was not redirected to the account page they changed after editing its info!")


class TestEditAccountAsInstructor(TestCase):

    def setUp(self):
        self.Instructor = User.objects.create_user('test1', password='test1')
        self.Instructor.save()
        make_instructor(self.Instructor.account)
        self.ArbitraryUser = User.objects.create_user('test2', password='test2')

    def test_edit_own_account_info_as_instructor(self):
        client = Client()
        client.login(username='test1', password='test1')

        response = client.post(f'/accounts/{self.Instructor.id}/update/',
                               {'first_name': 'test1', 'last_name': 'test1', 'email': 'test@test.com',
                                'phone_number': '+12624242825'}, follow=True)

        account_id = response.context['object'].user.id

        self.assertEqual(self.Instructor.id, account_id,
                         msg="User was not redirected to their account page after they changed its info!")

    def test_edit_other_account_as_instructor(self):
        client = Client()
        client.login(username='test1', password='test1')

        response = client.post(f'/accounts/{self.ArbitraryUser.id}/update/',
                               {'first_name': 'test1', 'last_name': 'test1', 'email': 'test@test.com',
                                'phone_number': '+12624242825'}, follow=True)

        self.assertEqual(response.status_code, 403, msg="User wasnt forbidden from changing another users info!")


class TestEditAccountAsTA(TestCase):

    def setUp(self):
        self.TA = User.objects.create_user('test1', password='test1')
        self.TA.save()
        make_ta(self.TA.account)
        self.ArbitraryUser = User.objects.create_user('test2', password='test2')

    def test_edit_own_account_info_as_instructor(self):
        client = Client()
        client.login(username='test1', password='test1')

        response = client.post(f'/accounts/{self.TA.id}/update/',
                               {'first_name': 'test1', 'last_name': 'test1', 'email': 'test@test.com',
                                'phone_number': '+12624242825'}, follow=True)

        account_id = response.context['object'].user.id

        self.assertEqual(self.TA.id, account_id,
                         msg="User was not redirected to their account page after they changed its info!")

    def test_edit_other_account_as_instructor(self):
        client = Client()
        client.login(username='test1', password='test1')

        response = client.post(f'/accounts/{self.ArbitraryUser.id}/update/',
                               {'first_name': 'test1', 'last_name': 'test1', 'email': 'test@test.com',
                                'phone_number': '+12624242825'}, follow=True)

        self.assertEqual(response.status_code, 403, msg="User wasnt forbidden from changing another users info!")
