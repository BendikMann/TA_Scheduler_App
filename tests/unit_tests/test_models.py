from collections import namedtuple

import phonenumbers.phonenumberutil
from django.test import TestCase

from django.contrib.auth.models import User
import Factories
import TA_Scheduler.models
from TA_Scheduler.models import UsAddress
from TA_Scheduler.models import Account


class TestModels(TestCase):

    def setUp(self):
        UsAddress.objects.create(state="WI", city="Milwaukee", street_address="3200 N Cramer St", zip_code="53211")
        User.objects.create(username="a", password="password", email="lebron@gmail.com", first_name="Lebron", last_name="James")

    def test_update_state_default(self):
        us_address = UsAddress.objects.get()
        self.assertEqual(True, us_address.update_state("NY"), "update_state didnt return True when state was changed")
        self.assertEqual("NY", us_address.state, "UsAddress state was not changed when update_state was called")

    def test_update_state_same_state(self):
        us_address = UsAddress.objects.get()
        self.assertEqual(True, us_address.update_state("WI"), "update_state didnt return true when trying to change state to the current state")
        self.assertEqual("WI", us_address.state, "UsAddress state was  changed when update_state was called with the same state")

    def test_update_state_invalid_state(self):
        us_address = UsAddress.objects.get()
        self.assertEqual(False, us_address.update_state("dsfgdfgdf"),
                         "update_state failed to return False when the input was invalid")
        self.assertEqual("WI", us_address.state,
                         "UsAddress state was  changed when update_state was called with an invalid state")

    def test_update_city_default(self):
        us_address = UsAddress.objects.get()
        self.assertEqual(True, us_address.update_city("London"), "update_city didnt return true when city was changed")
        self.assertEqual("London", us_address.city, "update_city didnt change city")

    def test_update_city_same(self):
        us_address = UsAddress.objects.get()
        self.assertEqual(True, us_address.update_city("Milwaukee"), "update_city didnt return true when city was changed to the same city")
        self.assertEqual("Milwaukee", us_address.city, "update_city changed city when it was supposed to remain the same")

    def test_update_city_invalid(self):
        us_address = UsAddress.objects.get()
        self.assertFalse(us_address.update_city("""1234567890
        12345678901234567890123456789012345678901234567890
        12345678901234567890123456789012345678901234567890
        123456789012345678901234567890"""        ), "passing update_city an invalid string fails to return False")
        self.assertEqual("Milwaukee", us_address.city, "Passing update_city an invalid string changes the city")

    def test_update_city_non_alpha_numeric(self):
        us_address = UsAddress.objects.get()
        self.assertEqual(False, us_address.update_city("@@"), "update_city didnt return false when a non-numeric string was passed")
        self.assertEqual("Milwaukee", us_address.city, "update_city changed city when it was supposed to remain the same")

    def test_update_street_address_default(self):
        us_address = UsAddress.objects.get()
        self.assertEqual(True, us_address.update_street_address("221B Baker St"), "update_street_address didnt return true when it was changed")
        self.assertEqual("221B Baker St", us_address.street_address, "update_street_address didnt change street address")

    def test_update_street_address_same(self):
        us_address = UsAddress.objects.get()
        self.assertEqual(True, us_address.update_street_address("3200 N Cramer St"), "update_street_address didnt return true when it was changed to the same address")
        self.assertEqual("3200 N Cramer St", us_address.street_address, "update_street_address changed street address when it shouldnt have")

    def test_update_street_address_invalid(self):
        us_address = UsAddress.objects.get()
        self.assertFalse(us_address.update_street_address("""1234567890
        12345678901234567890123456789012345678901234567890
        12345678901234567890123456789012345678901234567890
        123456789012345678901234567890
        """), "passing update_street_address an invalid string fails to return False")
        self.assertEqual("3200 N Cramer St", us_address.street_address, "Passing update_street_address an invalid string changes the street_address")

    def test_update_street_address_non_alpha_numeric(self):
        us_address = UsAddress.objects.get()
        self.assertEqual(False, us_address.update_street_address("@@"), "update_street_address didnt return false when a non-numeric string was passed")
        self.assertEqual("3200 N Cramer St", us_address.street_address, "update_street_address changed street address when it was supposed to remain the same")

    def test_update_zip_code_default(self):
        us_address = UsAddress.objects.get()
        self.assertEqual(True, us_address.update_zip_code("53151"), "update_zip_code failed to return True when zip code was changed")
        self.assertEqual("53151", us_address.zip_code, "update_zip_code didnt change the zip code as expected")

    def test_update_zip_code_same(self):
        us_address = UsAddress.objects.get()
        self.assertEqual(True, us_address.update_zip_code("53211"), "update_zip_code failed to return True when zip code was changed to the same thing")
        self.assertEqual("53211", us_address.zip_code, "update_zip_code didnt changed the zip code when it shouldnt have")

    def test_update_zip_code_invalid(self):
        us_address = UsAddress.objects.get()
        self.assertEqual(False, us_address.update_zip_code("dsfgdfgdf"),
                         "update_zip_code failed to return False when the input was invalid")
        self.assertEqual("53211", us_address.zip_code,
                         "UsAddress zip code was changed when update_zip_code was called with an invalid zip code")

    def test_update_first_name_default(self):
        account = Account.objects.get()
        self.assertEqual(True, account.update_first_name("bruh"), "update_first_name failed to return true when first name was changed")
        self.assertEqual("bruh", account.user.first_name, "update_first_name failed to change the first name to the expected result")

    def test_update_first_name_same(self):
        account = Account.objects.get()
        self.assertEqual(True, account.update_first_name("Lebron"), "update_first_name failed to return true when first name was changed to the same thing")
        self.assertEqual("Lebron", account.user.first_name, "update_first_name changed first name to something that was not expected")

    def test_update_first_name_invalid(self):
        account = Account.objects.get()
        self.assertFalse(account.update_first_name("""1234567890
        12345678901234567890123456789012345678901234567890
        12345678901234567890123456789012345678901234567890
        12345678901234567890123456789012345678901234567890
        """), "passing update_first_name an invalid string fails to return False")
        self.assertEqual("Lebron", account.user.first_name, "Passing update_first_name an invalid string changes the first name")

    def test_update_first_name_non_alpha_numeric(self):
        account = Account.objects.get()
        self.assertEqual(False, account.update_first_name("@@"), "update_first_name didnt return false when a non-numeric string was passed")
        self.assertEqual("Lebron", account.user.first_name, "update_first_name changed first name when it was supposed to remain the same")

    def test_update_last_name_default(self):
        account = Account.objects.get()
        self.assertEqual(True, account.update_last_name("bruh"), "update_last_name failed to return true when last name was changed")
        self.assertEqual("bruh", account.user.last_name, "update_last_name failed to change the last name to the expected result")

    def test_update_last_name_same(self):
        account = Account.objects.get()
        self.assertEqual(True, account.update_last_name("James"), "update_last_name failed to return true when last name was changed to the same thing")
        self.assertEqual("James", account.user.last_name, "update_last_name changed last name to something that was not expected")

    def test_update_last_name_invalid(self):
        account = Account.objects.get()
        self.assertFalse(account.update_last_name("""1234567890
        12345678901234567890123456789012345678901234567890
        12345678901234567890123456789012345678901234567890
        12345678901234567890123456789012345678901234567890
        """), "passing update_last_name an invalid string fails to return False")
        self.assertEqual("James", account.user.last_name, "Passing update_last_name an invalid string changes the last name")

    def test_update_last_name_non_alpha_numeric(self):
        account = Account.objects.get()
        self.assertEqual(False, account.update_last_name("@@"), "update_last_name didnt return false when a non-numeric string was passed")
        self.assertEqual("James", account.user.last_name, "update_last_name changed last name when it was supposed to remain the same")

    def test_update_phone_number_default(self):
        account = Account.objects.get()
        self.assertEqual(True, account.update_phone_number("+14155552671"), "update_phone_number failed to return true when it was changed")
        self.assertEqual("+14155552671", account.phone_number, "update_phone_number failed to change phone number to the expected result")

    def test_update_phone_number_same(self):
        account = Account.objects.get()
        account.update_phone_number("+14155552671")
        self.assertEqual(True, account.update_phone_number("+14155552671"), "update_phone_number failed to return true when it was changed to the same thing")
        self.assertEqual("+14155552671", account.phone_number, "update_phone_number changed the phone number when it wasnt expected to")

    def test_update_phone_number_invalid(self):
        account = Account.objects.get()
        account.update_phone_number("+14155552671")
        with self.assertRaises(phonenumbers.phonenumberutil.NumberParseException):
            self.assertFalse(account.update_phone_number("ygvyvyvygvyg"), "Passing an invalid phone number to update_phone_number failed to return False")
        self.assertEqual("+14155552671", account.phone_number, "Passing an invalid phone number to update_phone_number changed the phone number")
    def test_get_public_info(self):
        account = Account.objects.get()
        self.assertEqual(account.user.first_name, account.get_public_info().first_name, "get_public_info failed to return a named tuple that was correct")
        self.assertEqual(account.user.last_name, account.get_public_info().last_name, "get_public_info failed to return a named tuple that was correct")