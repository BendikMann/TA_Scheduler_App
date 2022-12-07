from django.contrib.auth.models import Group
from TA_Scheduler.models import *

app_name: str = "Ta_Scheduler"

# you are probably looking here because you don't remember how to setup migrations
# after clearing the database.
# 1) delete all migrations and the db itself.
# 2) in manage.py console
#   a) makemigrations
#   b) makemigrations TA_Scheduler --name make_groups --empty
# 3) in the make_groups migration
#   a) add the text migrations.RunPython(TA_Scheduler.groups.init_groups)
#       in the operations section.

# To make a long story short:
# Django permissions and groups are the most asinine implementation for
# permissions I have ever seen if you want to *programmatically* do them

def init_groups(apps, schema_migration):
    """
    Creates the required groups.
    :param apps:
    :param schema_migration:
    :return:
    """

    AdminGroup: Group = Group(name='Admin')
    InstructorGroup: Group = Group(name='Instructor')
    TAGroup: Group = Group(name='TA')
    AdminGroup.save()
    InstructorGroup.save()
    TAGroup.save()


