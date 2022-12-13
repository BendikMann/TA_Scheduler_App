from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views import View

from TA_Scheduler.models import Course
from TA_Scheduler.user import is_admin, get_all_users


class HomeView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'adminHomepage.html'

    def test_func(self):
        return is_admin(self.request.user)

    def get(self, request):

        courses = Course.objects.all()
        return render(request, self.template_name, {"users": get_all_users(), "courses": courses})

    pass


