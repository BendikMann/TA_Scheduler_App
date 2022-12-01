from django.test import TestCase

from django.contrib.auth.models import User
import Factories
import TA_Scheduler.models
from TA_Scheduler.models import UsAddress
from TA_Scheduler.models import Account


class TestModels(TestCase):

    def setUp(self):
        UsAddress.objects.create(state="WI", city="Milwaukee", street_address="3200 N Cramer St.", zip_code="53211")
        User.objects.create(username="a", password="password", email="lebron@gmail.com", first_name="Lebron", last_name="James")

    def test_update_state_default(self):
        us_address = UsAddress.objects.get()
        self.assertEqual(True, us_address.update_state("NY"), "update_state didnt return True when state was changed")
        self.assertEqual("NY", us_address.state, "UsAddress state was not changed when update_state was called")

    def test_update_state_same_state(self):
        us_address = UsAddress.objects.get()
        self.assertEqual(True, us_address.update_state("WI"),
                         "update_state didnt return true when trying to change state to the current state")
        self.assertEqual("WI", us_address.state,
                         "UsAddress state was  changed when update_state was called with the same state")

    def test_update_state_invalid_state(self):
        us_address = UsAddress.objects.get()
        self.assertEqual(False, us_address.update_state("dsfgdfgdf"),
                         "update_state failed to return False when the input was invalid")
        self.assertEqual("WI", us_address.state,
                         "UsAddress state was  changed when update_state was called with an invalid state")

    def test_update_state_not_us_country(self):
        pass

    def test_update_city_default(self):
        us_address = UsAddress.objects.get()
        self.assertEqual(True, us_address.update_city("London"), "update_city didnt return true when city was changed")
        self.assertEqual("London", us_address.city, "update_city didnt change city")

    def test_update_city_same(self):
        us_address = UsAddress.objects.get()
        self.assertEqual(True, us_address.update_city("Milwaukee"), "update_city didnt return true when city was changed to the same city")
        self.assertEqual("Milwaukee", us_address.city, "update_city changed city when it was supposed to remain the same")

    def test_update_street_address_default(self):
        us_address = UsAddress.objects.get()
        self.assertEqual(True, us_address.update_street_address("221B Baker St."), "update_street_address didnt return true when it was changed")
        self.assertEqual("221B Baker St.", us_address.street_address, "update_street_address didnt change street address")

    def test_update_street_address_same(self):
        us_address = UsAddress.objects.get()
        self.assertEqual(True, us_address.update_street_address("3200 N Cramer St."), "update_street_address didnt return true when it was changed to the same address")
        self.assertEqual("3200 N Cramer St.", us_address.street_address, "update_street_address changed street address when it shouldnt have")

    def test_update_zip_code_default(self):
        us_address = UsAddress.objects.get()
        self.assertEqual(True, us_address.update_zip_code("53151"), "update_zip_code failed to return True when zip code was changed")
        self.assertEqual("53151", us_address.zip_code, "update_zip_code didnt change the zip code as expected")

    def test_update_zip_code_same(self):
        us_address = UsAddress.objects.get()
        self.assertEqual(True, us_address.update_zip_code("53211"), "update_zip_code failed to return True when zip code was changed to the same thing")
        self.assertEqual("53211", us_address.zip_code, "update_zip_code didnt changed the zip code when it shouldnt have")

    def test_update_zip_code_invalid(self):
        pass

    def test_update_first_name_default(self):
        pass

    def test_update_first_name_same(self):
        pass

    def test_update_first_name_invalid(self):
        pass

    def test_update_last_name_default(self):
        pass

    def test_update_last_name_same(self):
        pass

    def test_update_last_name_invalid(self):
        pass

    def test_update_phone_number_default(self):
        pass

    def test_update_phone_number_same(self):
        pass

    def test_update_phone_number_invalid(self):
        pass
