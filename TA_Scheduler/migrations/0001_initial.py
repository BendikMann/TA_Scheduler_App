# Generated by Django 4.1.3 on 2022-12-09 01:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import localflavor.us.models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term_type', models.CharField(choices=[('spr', 'Spring'), ('fal', 'fall'), ('win', 'winterim'), ('sum', 'summer')], default='fal', max_length=3)),
                ('term_year', models.CharField(choices=[('2022', '2022'), ('2023', '2023'), ('2024', '2024')], default='2022', max_length=4)),
                ('course_number', models.CharField(max_length=5)),
                ('subject', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField(null=True)),
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
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('address', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='TA_Scheduler.usaddress')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_id', models.CharField(max_length=6)),
                ('section', models.CharField(max_length=4)),
                ('type', models.CharField(choices=[('LEC', 'Lecture'), ('DIS', 'Discussion'), ('LAB', 'Lab')], default='LAB', max_length=3)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('assigned_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TA_Scheduler.course')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='assigned_people',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
