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
        create_address = client.post(f'/address/create/', {'state': 'WI', 'city': 'Milwaukee', 'street_address': 'A very real street', 'zip_code': '53201'}, follow=True)

        self.assertEqual('account/view_account.html', create_address.template_name[0], msg="After address is created user should be redirected to the view of that address.")
        self.assertTrue(Account.objects.get(user_id=self.Admin.id).address.id, msg="Address was not set!")

    def test_CreateAddressForOther(self):
        client = Client()
        client.login(username='test1', password='test1')
        view_account = client.get(f'/accounts/{self.ArbitraryUser.account.id}/view/')
        self.assertEqual(self.ArbitraryUser.account.id, client.session['account_id_to_change'], msg='Session was not saved!')
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






