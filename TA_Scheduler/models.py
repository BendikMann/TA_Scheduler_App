from collections import namedtuple

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import ModelForm
from localflavor.us.models import USStateField, USZipCodeField
from phonenumber_field.modelfields import PhoneNumberField
import phonenumbers
from localflavor.us import us_states

# This model uses an extension of django which makes validation and form creation easier.
# See: https://github.com/django/django-localflavor
class UsAddress(models.Model):
    state = USStateField(default='WI')
    city = models.CharField(default='Milwaukee', max_length=128)
    street_address = models.CharField(max_length=128)
    zip_code = USZipCodeField(default='53201')

    def update_state(self, state: str) -> bool:
        # simple sanitization
        state = state.strip().upper()

        # make a list of all states that match our state input.
        state_exists_in_us_states = len([(x, y) for x, y in us_states.US_STATES if state in x]) > 0
        if state_exists_in_us_states:  # if we have more than zero states in that list, it must be valid.
            self.state = state
            self.save()
        return state_exists_in_us_states

    def update_city(self, city: str) -> bool:
        if len(city) <= 128 and city.isalnum():
            self.city = city
            self.save()
            return True
        return False

    def update_street_address(self, street_address: str) -> bool:
        if len(street_address) <= 128 and street_address.isalnum():
            self.street_address = street_address
            self.save()
            return True
        return False

    def update_zip_code(self, zip_code: str) -> bool:
        if (len(zip_code) == 5) or (len(zip_code) == 9):
            # splits the zip code by a - to check for zip+4 (54444-5555)
            zip_code_split = zip_code.split("-")
            # checks if the zip code is split into either [54444] or [54444, 5555] else return false
            if len(zip_code_split) == 1:
                if len(zip_code_split[0]) == 5 and zip_code_split[0].isnumeric():
                    self.zip_code = zip_code
                    self.save()
                    return True
            elif len(zip_code_split) == 2:
                if len(zip_code_split[0]) == 5 and zip_code_split[0].isnumeric() and zip_code_split[1].isnumeric():
                    self.zip_code = zip_code
                    self.save()
                    return True
        return False

    def __str__(self):
        return f"{self.street_address}\n" \
               f"{self.city}, {self.state} {self.zip_code}\n" \
               f"USA"

# This clever way of extending User was found here:
#   https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.OneToOneField(UsAddress, null=True, on_delete=models.CASCADE)
    # This is an extension of django which makes validation and form creation easier.
    # See: https://django-phonenumber-field.readthedocs.io/en/latest/index.html
    phone_number = PhoneNumberField(blank=True)

    def update_first_name(self, first_name: str) -> bool:
        if len(first_name) <= 150 and first_name.isalnum():
            self.user.first_name = first_name
            self.save()
            return True
        return False

    def update_last_name(self, last_name: str) -> bool:
        if len(last_name) <= 150 and last_name.isalnum():
            self.user.last_name = last_name
            self.save()
            return True
        return False

    def update_phone_number(self, phone_number: str) -> bool:
        parsed_phone_number = phonenumbers.parse(phone_number)
        if phonenumbers.is_valid_number(parsed_phone_number):
            self.phone_number = phone_number
            self.save()
            return True
        return False

    def get_public_info(self) -> namedtuple("public_info", ["first_name", "last_name"]):
        public_info = namedtuple("public_info", ["first_name", "last_name"])
        return public_info(self.user.first_name, self.user.last_name)

    def __str__(self):
        return f"User: {self.user.first_name} {self.user.last_name} {self.user.username} Group: {self.user.groups.first()}\n" \
               f"Email: {self.user.email}\n" \
               f"Phone Number: {self.phone_number} \n" \
               f"{self.address}"

        pass



class UserModelForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
class AccountModelForm(ModelForm):
    class Meta:
        model = Account
        fields = ['phone_number']

class Course(models.Model):
    # instructor foreign key
    instructor = models.ManyToManyField(Account)

    # represented as a string because some courses might have a letter after their course numbers (i.e. 422G)
    course_number = models.CharField(max_length=5)

    # course subject (i.e. COMPSCI)
    subject = models.CharField(max_length=10)

    section = models.CharField(max_length=5)

    # course name (i.e Compsci 361 has a name of Introduction to Software Engineering)
    name = models.CharField(max_length=30)

    def __str__(self):
        # Turns out there is a quite a bit that we need to process.
        instructors = ''
        for instructor in self.instructor.all():
            instructors += f"{instructor.user.first_name} {instructor.user.last_name}"

        return f"Instructors: {instructors}\n" \
               f"Number: {self.course_number} \n" \
               f"Subject: {self.subject} \n" \
               f"Section: {self.section}\n" \
               f"Name: {self.name}\n"


class Lab(models.Model):
    section = models.CharField(max_length=5)
    ta = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.section} TA: {self.ta.user.first_name} {self.ta.user.last_name} Course: {self.course.course_number}\n"

        pass

# Whenever we create a user, also create a account attached to it.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)


# Whenever we save a User, also update the account attached to it.
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.account.save()
