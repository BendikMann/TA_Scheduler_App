from django.contrib.auth.models import User
from django.test import TestCase, Client
from Factories import *
from TA_Scheduler.user import make_admin, make_instructor, make_ta
from TA_Scheduler.models import Account


class TestLogIn(TestCase):
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

    def test_AdminWrongPassword(self):
        client = Client()
        for i in self.wrong_passwords:
            self.assertFalse(client.login(username=self.Admin.username, password=i))
            resp = client.get(f'/accounts/{self.Admin.account.id}/view/')
            self.assertNotEqual(resp.status_code, 200, "Get accounts view returned status code 200 (OK) after "
                                                       "using wrong admin password")

    def test_AdminWrongUsername(self):
        client = Client()
        for i in self.wrong_passwords:
            self.assertFalse(client.login(username=i, password="admin1"))
            resp = client.get(f'/accounts/{self.Admin.account.id}/view/')
            self.assertNotEqual(resp.status_code, 200, "Get accounts view returned status code 200 (OK) after "
                                                       "using wrong admin username")

    def test_InstructorCorrectInfo(self):
        client = Client()
        self.assertTrue(client.login(username=self.Instructor.username, password='instructor1'), "Successful "
                                                                                                 "instructor login "
                                                                                                 "doesn't return true")
        resp = client.get(f'/accounts/{self.Instructor.account.id}/view/')
        self.assertEqual(resp.status_code, 200, "Get accounts view did not return status code 200 (OK) after "
                                                "successful instructor login")

    def test_InstructorWrongPassword(self):
        client = Client()
        for i in self.wrong_passwords:
            self.assertFalse(client.login(username=self.Instructor.username, password=i))
            resp = client.get(f'/accounts/{self.Instructor.account.id}/view/')
            self.assertNotEqual(resp.status_code, 200, "Get accounts view returned status code 200 (OK) after "
                                                       "using wrong instructor password")

    def test_InstructorWrongUsername(self):
        client = Client()
        for i in self.wrong_passwords:
            self.assertFalse(client.login(username=i, password="instructor1"))
            resp = client.get(f'/accounts/{self.Instructor.account.id}/view/')
            self.assertNotEqual(resp.status_code, 200, "Get accounts view returned status code 200 (OK) after "
                                                       "using wrong instructor username")

    def test_TaCorrectInfo(self):
        client = Client()
        self.assertTrue(client.login(username=self.Ta.username, password='ta1'), "Successful ta login doesn't return "
                                                                                 "true")
        resp = client.get(f'/accounts/{self.Ta.account.id}/view/')
        self.assertEqual(resp.status_code, 200, "Get accounts view did not return status code 200 (OK) after "
                                                "successful ta login")

    def test_TaWrongPassword(self):
        client = Client()
        for i in self.wrong_passwords:
            self.assertFalse(client.login(username=self.Ta.username, password=i))
            resp = client.get(f'/accounts/{self.Ta.account.id}/view/')
            self.assertNotEqual(resp.status_code, 200, "Get accounts view returned status code 200 (OK) after "
                                                       "using wrong ta password")

    def test_TaWrongUsername(self):
        client = Client()
        for i in self.wrong_passwords:
            self.assertFalse(client.login(username=i, password="ta1"))
            resp = client.get(f'/accounts/{self.Instructor.account.id}/view/')
            self.assertNotEqual(resp.status_code, 200, "Get accounts view returned status code 200 (OK) after "
                                                       "using wrong ta username")


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
