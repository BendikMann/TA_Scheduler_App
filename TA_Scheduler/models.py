from collections import namedtuple

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from localflavor.us.models import USStateField, USZipCodeField
from phonenumber_field.modelfields import PhoneNumberField


# This model uses an extension of django which makes validation and form creation easier.
# See: https://github.com/django/django-localflavor
class UsAddress(models.Model):
    state = USStateField(default='WI')
    city = models.CharField(default='Milwaukee', max_length=128)
    street_address = models.CharField(max_length=128)
    zip_code = USZipCodeField(default='53201')

    def update_state(self, state: str) -> bool:
        pass

    def update_postal_code(self, postal_code: str) -> bool:
        pass

    def update_street_address(self, street_address: str) -> bool:
        pass

    def update_zip_code(self, zip_code: str) -> bool:
        pass

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
        pass

    def update_last_name(self, last_name: str) -> bool:
        pass

    def update_phone_number(self, phone_number: str) -> bool:
        pass

    def get_public_info(self) -> namedtuple("public_info", ["first_name", "last_name"]):
        pass

    def __str__(self):
        return f"User: {self.user.first_name} {self.user.last_name} {self.user.username} Group: {self.user.groups.first()}\n" \
               f"Email: {self.user.email}\n" \
               f"Phone Number: {self.phone_number} \n" \
               f"{self.address}"

        pass


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
