from collections import namedtuple

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from localflavor.us.models import USPostalCodeField, USStateField, USZipCodeField
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


# This model uses an extension of django which makes validation and form creation easier.
# See: https://github.com/django/django-localflavor
class UsAddress(models.Model):
    state = USStateField(default="WI", blank=True)
    postal_code = USPostalCodeField(blank=True)
    street_address = models.CharField(max_length=128)
    zip_code = USZipCodeField(blank=True)

    def update_state(self, state: str) -> bool:
        pass

    def update_postal_code(self, postal_code: str) -> bool:
        pass

    def update_street_address(self, street_address: str) -> bool:
        pass

    def update_zip_code(self, zip_code: str) -> bool:
        pass


# This clever way of extending User was found here:
#   https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.OneToOneField(UsAddress, null=True, on_delete=models.CASCADE)
    # This is an extension of django which makes validation and form creation easier.
    # See: https://django-phonenumber-field.readthedocs.io/en/latest/index.html
    phone_number = PhoneNumberField(blank=True)

    def update_first_name(self, first_name: str) -> bool:
        pass

    def update_last_name(self, last_name: str) -> bool:
        pass

    def update_phone_number(self, phone_number: str) -> bool:
        pass

    def get_public_info(self) -> namedtuple("public_info", ["first_name", "last_name"]):
        pass


class Lab(models.Model):
    section = models.CharField(max_length=5)
    ta = models.OneToOneField(Account, on_delete=models.SET_NULL)
    course = models.OneToOneField(Course, on_delete=models.SET_NULL)


# Whenever we create a user, also create a account attached to it.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)


# Whenever we save a User, also update the account attached to it.
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.account.save()

class Course(models.Model):
    # TODO: Actually make course Model
    pass

class LabSection(models.Model):
    # TODO: Actually make Lab Section model.
    pass