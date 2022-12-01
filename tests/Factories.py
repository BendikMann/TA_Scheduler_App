import random

import factory.django
from django.db.models.signals import post_save
from localflavor.us import us_states
from django.contrib.auth.models import Group
from TA_Scheduler import models

# Use these to make 'mock' objects for the database that are robust.


class LabFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Lab

    section = factory.Faker('random_letters', length=5)

    @factory.post_generation
    def ta_set(self, create, extracted, **kwargs):
        if not create:
            return
        # get the list of instructors and add an arbitrary amount of instructors to each course.
        tas = models.Account.objects.filter(user__groups__name="TA").all()
        if len(tas) > 0:
            self.ta = course=random.choice(tas)
    @factory.post_generation
    def course_set(self, create, extracted, **kwargs):
        if not create:
            return

        courses = models.Course.objects.all()
        if len(courses) > 0:
            self.course = random.choice(courses)


class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Course

    course_number = factory.Faker('numerify', text='#####')
    subject = factory.Faker('random_letters', length=10)
    section = factory.Faker('random_letters', length=5)
    name = factory.Faker('bs')

    @factory.post_generation
    def course_instructor_set(self, create, extracted, **kwargs):
        if not create:
            return
        #get the list of instrucctors and add an arbitrary amount of instructors to each course.
        instructors = models.Account.objects.filter(user__groups__name="Instructor")
        for instructor in random.choices(instructors, k=random.randint(0, len(instructors))):
            self.instructor.add(instructor)


class UsAddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.UsAddress
    zip_code = factory.Faker('postcode')
    street_address = factory.Faker('street_address')
    city = factory.Faker('city')
    state = random.choice(us_states.US_STATES)[0]


@factory.django.mute_signals(post_save)
class _AccountFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Account

    phone_number = factory.Faker('phone_number')
    address = factory.SubFactory(UsAddressFactory)
    pass


@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    with factory.django.mute_signals(post_save):
        class Meta:
            model = models.User
        first_name = factory.Faker('first_name')
        last_name = factory.Faker('last_name')
        email = factory.Faker('email')
        username = factory.Sequence(lambda n: f"GenericUsername{n}")

        account = factory.RelatedFactory(_AccountFactory, factory_related_name='user')

        @factory.post_generation
        def groups_set(self, create, extracted, **kwargs):
            if not create:
                return

            group: Group = random.choices(Group.objects.all())[0]
            group.user_set.add(self)




