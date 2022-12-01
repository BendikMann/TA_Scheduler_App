# Generated by Django 4.1.3 on 2022-11-30 23:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import localflavor.us.models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_number', models.CharField(max_length=5)),
                ('subject', models.CharField(max_length=10)),
                ('section', models.CharField(max_length=5)),
                ('name', models.CharField(max_length=30)),
                ('instructor', models.ManyToManyField(to='TA_Scheduler.account')),
            ],
        ),
        migrations.CreateModel(
            name='UsAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', localflavor.us.models.USStateField(default='WI', max_length=2)),
                ('city', models.CharField(default='Milwaukee', max_length=128)),
                ('street_address', models.CharField(max_length=128)),
                ('zip_code', localflavor.us.models.USZipCodeField(default='53201', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Lab',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.CharField(max_length=5)),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='TA_Scheduler.course')),
                ('ta', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='TA_Scheduler.account')),
            ],
        ),
        migrations.AddField(
            model_name='account',
            name='address',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='TA_Scheduler.usaddress'),
        ),
        migrations.AddField(
            model_name='account',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
