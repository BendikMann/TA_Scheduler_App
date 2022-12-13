from django.core.exceptions import PermissionDenied

import TA_Scheduler.models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView

from django.views.generic.edit import CreateView, DeleteView, UpdateView

from TA_Scheduler.forms import NewUserCreationForm
from TA_Scheduler.models import *
from TA_Scheduler.user import *


# Create your views here.
# Views moved to doc. 


