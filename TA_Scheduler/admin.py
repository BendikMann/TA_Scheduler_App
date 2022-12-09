from django.contrib.auth.admin import admin

from TA_Scheduler.models import *

from django.contrib import admin

admin.site.register(User)
admin.site.register(UsAddress)
admin.site.register(Course)

