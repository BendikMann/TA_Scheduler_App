# Generated by Django 4.1.3 on 2022-12-08 16:05

from django.db import migrations

import TA_Scheduler.groups


class Migration(migrations.Migration):

    dependencies = [
        ('TA_Scheduler', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(TA_Scheduler.groups.init_groups)
    ]