from django.shortcuts import render
from django.views import View
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
class login(UserCreationForm):

    def get(self, request):
        return render(request, "registration/login.html")
