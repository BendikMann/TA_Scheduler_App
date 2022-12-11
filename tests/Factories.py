import random
from datetime import datetime, timedelta

import factory.django
import factory.fuzzy
from django.db.models.signals import post_save
from localflavor.us import us_states
from django.contrib.auth.models import Group
from TA_Scheduler import models, model_choice_data
from django.contrib.auth.hashers import make_password


# Use these to make 'mock' objects for the database that are robust.
Section_Types = [model_choice_data.SectionChoices.LAB,
                 model_choice_data.SectionChoices.LECTURE,
                 model_choice_data.SectionChoices.DISCUSSION]

Course_Name = [model_choice_data.CourseChoices.YEAR2022,
               model_choice_data.CourseChoices.YEAR2023,
               model_choice_data.CourseChoices.YEAR2024]

Course_Type = [model_choice_data.CourseChoices.FALL,
               model_choice_data.CourseChoices.WINTERIM,
               model_choice_data.CourseChoices.SPRING,
               model_choice_data.CourseChoices.SUMMER]

class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Course

    term_type = factory.fuzzy.FuzzyChoice([i[0] for i in model_choice_data.CourseChoices.TERM_NAMES])
    term_year = factory.fuzzy.FuzzyChoice([i[0] for i in model_choice_data.CourseChoices.TERM_YEAR])

    course_number = factory.Faker('numerify', text='#####')
    # TODO: Make believable course subjects
    subject = factory.Faker('bothify', text='????????')
    name = factory.Faker('bs')
    description = factory.Faker("paragraph", nb_sentences=5)

    @factory.post_generation
    def course_people_sections_set(self, create, extracted, **kwargs):
        if not create:
            return

        #create a random number of sections from 0 to 20.
        for i in range(0, random.randint(0, 20)):
            _SectionFactory(course=self)


        # get the list of instructors and add an arbitrary amount of instructors to each course.
        instructors = models.User.objects.filter(groups__name='Instructor')
        instr_num = random.randint(0, min(3, len(instructors)))

        for instructor in random.choices(instructors, k=instr_num):
            self.assigned_people.add(instructor)

        # get the list of tas and add an arbitrary number of TA's too.
        ta = models.User.objects.filter(groups__name='TA')
        ta_num = random.randint(0, min(7, len(ta)))
        for ta in random.choices(ta, k=ta_num):
            self.assigned_people.add(ta)

        #of the sections that are labs, add 0 or 1 tas to them.
        ta_sections = self.section_set.filter(course__section__type=model_choice_data.SectionChoices.LAB)
        tas = self.assigned_people.filter(groups__name='TA')

        for ta_section in ta_sections:
            if random.randint(0, 1) == 1 and len(tas) != 0:
                ta_section.assigned_user = random.choice(tas)



class _SectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Section

    class_id = factory.Faker('numerify', text='#####')
    section = factory.Faker('bothify', text='###?')
    type = factory.fuzzy.FuzzyChoice([i[0] for i in model_choice_data.SectionChoices.SECTION_CHOICES])
    meet_monday = factory.fuzzy.FuzzyChoice([True, False])
    meet_tuesday = factory.fuzzy.FuzzyChoice([True, False])
    meet_wednesday = factory.fuzzy.FuzzyChoice([True, False])
    meet_thursday = factory.fuzzy.FuzzyChoice([True, False])
    meet_friday = factory.fuzzy.FuzzyChoice([True, False])
    meet_start = factory.Faker('date_time')
    @factory.post_generation
    def make_meeting_times(self, created, extracted, **kwargs):
        self.meet_end = self.meet_start + timedelta(minutes=random.choice([50, 60, 80, 120]))



class UsAddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.UsAddress

    zip_code = factory.Faker('postcode')
    street_address = factory.Faker('street_address')
    city = factory.Faker('city')
    state = factory.fuzzy.FuzzyChoice([i[0] for i in us_states.US_STATES])

class UserFactory(factory.django.DjangoModelFactory):
    with factory.django.mute_signals(post_save):
        class Meta:
            model = models.User

        first_name = factory.Faker('first_name')
        last_name = factory.Faker('last_name')
        email = factory.Faker('email')
        password = factory.LazyFunction(lambda: make_password("password"))
        address = factory.SubFactory(UsAddressFactory)
        phone_number = factory.Faker('phone_number')
        @factory.post_generation
        def groups_set(self, create, extracted, **kwargs):
            if not create:
                return

            group: Group = random.choice(Group.objects.all())
            group.user_set.add(self)
