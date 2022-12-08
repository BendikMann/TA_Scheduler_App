from django.contrib.auth.models import User
from django.test import TestCase, Client
from Factories import *
from TA_Scheduler.user import make_admin
from TA_Scheduler.models import Account


class TestAddressCreation(TestCase):

    def setUp(self):
        UserFactory()
        self.Admin = User.objects.create_user('test1', password='test1')
        self.Admin.save()
        make_admin(self.Admin.account)
        UserFactory()
        self.ArbitraryUser = User.objects.create_user('test2', password='test2')

    def test_CreateAddressAdminSelf(self):
        client = Client()
        client.login(username='test1', password='test1')
        view_account = client.get(f'/accounts/{self.Admin.account.id}/view/')
        self.assertEqual(self.Admin.account.id, client.session['account_id_to_change'], msg='Session was not saved!')
        create_address = client.post(f'/address/create/',
                                     {'state': 'WI', 'city': 'Milwaukee', 'street_address': 'A very real street',
                                      'zip_code': '53201'}, follow=True)

        self.assertEqual('account/view_account.html', create_address.template_name[0],
                         msg="After address is created user should be redirected to the view of that address.")
        self.assertTrue(Account.objects.get(user_id=self.Admin.id).address.id, msg="Address was not set!")

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
        self.assertTrue(Account.objects.get(user_id=self.ArbitraryUser.id).address.id, msg="Address was not set!")

    def test_CreateAddressNoContext(self):
        client = Client()
        client.login(username='test1', password='test1')
        create_address = client.post(f'/address/create/',
                                     {'state': 'WI', 'city': 'Milwaukee', 'street_address': 'A very real street',
                                      'zip_code': '53201'}, follow=True)
        self.assertEqual(create_address.status_code, 403, "The user went straight to the create page and we don't "
                                                          "have the context for who's address we should create.")
        pass

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

        create_account = client.post(f'/accounts/register/',
                                     {'username': 'test4', 'password1': 'MegaSuperPassw00rd',
                                      'password2': 'MegaSuperPassw00rd'}, follow=True)
        account_id = create_account.context['object'].user.id

        response = client.get(f'/account/{account_id}/delete', follow=True)
        response = client.get({f'/accounts/{account_id}/view'})

        self.assertNotEqual(response.status_code, 404, "User was deleted even though the operation was canceled!")
