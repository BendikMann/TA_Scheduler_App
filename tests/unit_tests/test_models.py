from django.test import TestCase
from TA_Scheduler.models import UsAddress
from TA_Scheduler.models import Account


class TestModels(TestCase):

    def setUp(self):
        UsAddress.objects.create(state="WI", postal_code="00851", street_address="3200 North Cramer St", zip_code="53211")

    def test_update_state_default(self):
        pass

    def test_update_state_same_state(self):
        pass

    def test_update_state_invalid_state(self):
        pass

    def test_update_state_not_us_country(self):
        pass

    def test_update_postal_code_default(self):
        pass

    def test_update_postal_code_same(self):
        pass

    def test_update_postal_code_invalid(self):
        pass

    def test_update_street_address_default(self):
        pass

    def test_update_street_address_same(self):
        pass

    def test_update_street_address_invalid(self):
        pass

    def test_update_zip_code_default(self):
        pass

    def test_update_zip_code_same(self):
        pass

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
