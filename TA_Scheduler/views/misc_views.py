from abc import ABC

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from TA_Scheduler.forms import EmailForm
from TA_Scheduler.models import Course, Section
from TA_Scheduler.user import is_admin, get_all_users, is_instructor, is_ta, Admin, Instructor


class HomeView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'adminHomepage.html'

    def test_func(self):
        return is_admin(self.request.user)

    def get(self, request):
        courses = Course.objects.all()
        sections = Section.objects.all()
        return render(request, self.template_name, {"users": get_all_users(), "courses": courses, "sections": sections})

    pass


class InstructorHomeView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'instructorHomepage.html'

    def test_func(self):
        return is_instructor(self.request.user)

    def get(self, request):
        courses = Course.objects.filter(assigned_people__id=self.request.user.id)
        sections = Section.objects.filter(assigned_user__id=self.request.user.id)
        return render(request, self.template_name,
                      {"users": Instructor(self.request.user).get_assigned_tas(), "courses": courses,
                       "sections": sections})

    pass


class TAHomeView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'taHomepage.html'

    def test_func(self):
        return is_ta(self.request.user)

    def get(self, request):
        courses = Course.objects.filter(assigned_people__id=self.request.user.id)
        sections = Section.objects.filter(assigned_user__id=self.request.user.id)
        return render(request, self.template_name, {"users": get_all_users(), "courses": courses, "sections": sections})

    pass


class Announcement(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'announcement.html'

    def test_func(self):
        return is_admin(self.request.user) or is_instructor(self.request.user)

    def get(self, request):
        email_form = EmailForm()
        return render(request, self.template_name, {'email_form': email_form})

    def post(self, request):
        email_form = EmailForm(request.POST)
        if email_form.is_valid():
            if is_admin(self.request.user):
                header = email_form.cleaned_data['header']
                content = email_form.cleaned_data['content']
                Admin(self.request.user).send_email(header, content)
                return redirect('home-page')

            elif is_instructor(self.request.user):
                header = email_form.cleaned_data['header']
                content = email_form.cleaned_data['content']
                Instructor(self.request.user).send_email(header, content)
                return redirect('home-page')


class EnterView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return is_admin(self.request.user) or is_instructor(self.request.user) or is_ta(self.request.user)

    def get(self, request):
        if is_admin(request.user):
            return redirect('/home/admin/')
        elif is_instructor(request.user):
            return redirect('/home/instructor/')
        elif is_ta(request.user):
            return redirect('/home/ta/')
        else:
            return False
