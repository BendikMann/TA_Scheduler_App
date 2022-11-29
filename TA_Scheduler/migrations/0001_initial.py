# Generated by Django 4.1.3 on 2022-11-29 18:38

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
            name='LabSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='UsAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', localflavor.us.models.USStateField(blank=True, default='WI', max_length=2)),
                ('postal_code', localflavor.us.models.USPostalCodeField(blank=True, max_length=2)),
                ('street_address', models.CharField(max_length=128)),
                ('zip_code', localflavor.us.models.USZipCodeField(blank=True, max_length=10)),
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