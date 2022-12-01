from django.contrib.auth.models import Group, Permission
from TA_Scheduler.models import *
app_name: str = "Ta_Scheduler"

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

    # migrations cannot access this stuff directly, so we need to do this instead.
    user: User = apps.get_model('auth', 'User')
    group: Group = apps.get_model('auth', 'Group')
    permission: Permission = apps.get_model('auth', 'Permission')
    # Groups are persistent, so all we need to do is run this once!
    AdminGroup: Group = Group(name='Admin')
    InstructorGroup: Group = Group(name='Instructor')
    TAGroup: Group = Group(name='TA')
    AdminGroup.save()
    InstructorGroup.save()
    TAGroup.save()

def init_group_perms():
    """
    Assigns the required perms to the
    :return:
    """
    # TODO: Complete at least the admin permissions.


    pass


def get_add_perm(permission: Permission, model: models) -> Permission:
    return permission.objects.get(codename=f"add_{model.__name__.lower()}")


def get_change_perm(permission, model: models):
    return permission.objects.get(codename=f"change_{model.__name__}")


def get_delete_perm(permission, model: models):
    return permission.objects.get(codename=f"delete_{model.__name__}")
    pass


def get_view_perm(permission, model: models):
    return permission.objects.get(codename=f"delete_{model.__name__}")

