from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.forms import ModelForm
import django.forms as forms
from django.utils.translation import gettext_lazy as _
from localflavor.us.models import USStateField, USZipCodeField
from phonenumber_field.modelfields import PhoneNumberField

from TA_Scheduler.model_choice_data import CourseChoices, SectionChoices


# This model uses an extension of django which makes validation and form creation easier.
# See: https://github.com/django/django-localflavor
class UsAddress(models.Model):
    state = USStateField(default='WI')
    city = models.CharField(default='Milwaukee', max_length=128)
    street_address = models.CharField(max_length=128)
    zip_code = USZipCodeField(default='53201')

    def __str__(self):
        return f"{self.street_address}\n" \
               f"{self.city}, {self.state} {self.zip_code}\n" \
               f"USA"


class CustomUserManager(BaseUserManager):
    """

    """

    def create_user(self, email, first_name, last_name, password=None, **other_fields):
        """
        Creates and saves a User with the given email and password.
        """

        # TODO: Unit tests and validation!
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            **other_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **other_fields):
        """
        Creates and saves a superuser with the given email and password.
        """

        user = self.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            **other_fields,

        )
        user.is_superuser = True  # All perms
        user.is_staff = True  # Admin portal
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email address',
                              unique=True,
                              max_length=255)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = PhoneNumberField(blank=True)
    address = models.OneToOneField(UsAddress, null=True, on_delete=models.CASCADE)

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def get_full_name(self):
        # The user is identified by their email address
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name

    def is_admin(self):
        return self.groups.filter(name='Admin').exists()

    def __str__(self):
        return f"User: {self.first_name} {self.last_name} Group: {self.groups.first()}\n" \
               f"Email: {self.email} Phone Number: {self.phone_number} \n" \
               f"{self.address}"


# This clever way of extending User was found here:
#   https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html

class UserModelForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number']


class Course(models.Model):
    assigned_people = models.ManyToManyField(User)

    term_type = models.CharField(max_length=3, choices=CourseChoices.TERM_NAMES,
                                 default=CourseChoices.FALL)

    term_year = models.CharField(max_length=4, choices=CourseChoices.TERM_YEAR, default=CourseChoices.YEAR2022)

    # represented as a string because some courses might have a letter after their course numbers (i.e. 422G)
    course_number = models.CharField(max_length=5)

    # course subject (i.e. COMPSCI)
    subject = models.CharField(max_length=10)

    # course name (i.e Compsci 361 has a name of Introduction to Software Engineering)
    name = models.CharField(max_length=30)

    # course description (because it's trivial to include)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        # Turns out there is a quite a bit that we need to process.
        self.assigned_people.filter(groups__name='TA')
        return f"{self.subject}-{self.course_number} {self.term_type} {self.term_year}\n" \
               f"{self.description} \n" \
               f"Assigned People:\n\n\n" \
               f"{*self.assigned_people.all(),}" \
               f"Sections: \n\n\n" \
               f"{*self.section_set.all(),}"


class CourseAssignModelForm(ModelForm):
    class Meta:
        model = Course
        fields = ['term_type']

    def __init__(self, *args, **kwargs):
        super(CourseAssignModelForm, self).__init__(*args, **kwargs)
        # filtering the instructor field to only include accounts with the group of TA or Instructor


class CourseModelForm(ModelForm):
    tas = forms.ModelMultipleChoiceField(queryset=User.objects.all(), required=False)
    instructors = forms.ModelMultipleChoiceField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Course
        fields = ['tas', 'instructors', 'term_type', 'term_year', 'course_number', 'subject', 'name', 'description']

    def __init__(self, *args, **kwargs):
        super(CourseModelForm, self).__init__(*args, **kwargs)
        # filtering the instructor field to only include accounts with the group of TA or Instructor
        self.fields['tas'].queryset = User.objects.filter(groups__name__in=['TA'])
        self.fields['instructors'].queryset = User.objects.filter(groups__name__in=['Instructor'])

        if self.instance.id is not None:
            self.fields['tas'].initial = [x.id for x in Course.objects.get(id=self.instance.id).assigned_people.filter(
                groups__name__in=['TA'])]
            self.fields['instructors'].initial = [x.id for x in
                                                  Course.objects.get(id=self.instance.id).assigned_people.filter(
                                                      groups__name__in=['Instructor'])]

class Section(models.Model):
    # A section MUST have a course assigned to it.
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    # A Section may have a user undefined for an arbitrary amount of time.
    assigned_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class_id = models.CharField(max_length=6)

    section = models.CharField(max_length=4)

    type = models.CharField(max_length=3, choices=SectionChoices.SECTION_CHOICES, default=SectionChoices.LAB)

    # TODO: meeting schedule
    meet_monday = models.BooleanField(default=False)
    meet_tuesday = models.BooleanField(default=False)
    meet_wednesday = models.BooleanField(default=False)
    meet_thursday = models.BooleanField(default=False)
    meet_friday = models.BooleanField(default=False)
    meet_start = models.TimeField(null=True)
    meet_end = models.TimeField(null=True)

    def __str__(self):
        return f" {self.class_id} {self.section} {self.type} " \
               f"{'' if self.assigned_user is None else self.assigned_user.first_name} " \
               f"{'' if self.assigned_user is None else self.assigned_user.last_name}\n"


class SectionModelForm(ModelForm):
    class Meta:
        model = Section
        fields = ['class_id', 'section', 'type', 'meet_start', 'meet_end', 'meet_monday',
                  'meet_tuesday', 'meet_wednesday', 'meet_thursday', 'meet_friday']


class AssignSectionModelForm(ModelForm):
    class Meta:
        model = Section
        fields = ['assigned_user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # filtering to show only Accounts which are a part of the associated course

        if self.instance.id is not None:
            self.fields['assigned_user'].queryset = User.objects.filter(course=self.instance.course)

            if self.instance.type == 'LEC':
                self.fields['assigned_user'].queryset = self.fields['assigned_user'].queryset.filter(groups__name__in=['Instructor'])
            else:
                self.fields['assigned_user'].queryset = self.fields['assigned_user'].queryset.filter(groups__name__in=['TA'])


    def clean(self):
        cleaned_data = super().clean()
        assigned_user = cleaned_data.get("assigned_user")
        section_type = cleaned_data.get("type")

        # checking the users group and preventing them from being assigned to sections they couldn't be a part of
        if assigned_user and assigned_user.groups.filter(name="Instructor").exists() and section_type == "LAB":
            raise ValidationError("Instructors cannot be assigned to lab sections.")
        if assigned_user and assigned_user.groups.filter(name="Instructor").exists() and section_type == "DIS":
            raise ValidationError("Instructors cannot be assigned to discussion sections.")
        if assigned_user and assigned_user.groups.filter(name="TA").exists() and section_type == "LEC":
            raise ValidationError("TAs cannot be assigned to lecture sections.")

        return cleaned_data
