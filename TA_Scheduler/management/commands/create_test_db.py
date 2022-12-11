from django.core.management.base import BaseCommand, CommandError

import Factories
import TA_Scheduler.models


class Command(BaseCommand):
    help = 'Creates the specified amount of instances to fill the database'

    def add_arguments(self, parser):
        parser.add_argument('--user_number', nargs='+', type=int)
        parser.add_argument('--course_number', nargs='+', type=int)

    def handle(self, *args, **option):
        user_count = option['user_number'][0] or 0
        course_count = option['course_number'][0] or 0

        for user in range(0, user_count):
            Factories.UserFactory()
        for course in range(0, course_count):
            Factories.CourseFactory()

        self.stdout.write(f"User now has {TA_Scheduler.models.Account.objects.count()} entries")
        self.stdout.write(f"Course now has {TA_Scheduler.models.Course.objects.count()} entries")
        self.stdout.write(f"Section now has {TA_Scheduler.models.Section.objects.count()} entries")