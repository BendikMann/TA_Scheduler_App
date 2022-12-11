from django.core.exceptions import PermissionDenied

import TA_Scheduler.models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView

from django.views.generic.edit import CreateView, DeleteView, UpdateView
from TA_Scheduler.models import *
from TA_Scheduler.user import *


# Create your views here.


class CreateAddress(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = UsAddress
    fields = '__all__'

    def get_account(self) -> Account:
        try:
            account_id = int(self.request.session.get('account_id_to_change'))
        except TypeError:
            raise PermissionDenied()
        account = Account.objects.get(id=account_id)
        return account

    def test_func(self):
        # User to create address for does not have an address and the one creating the address is an admin or the user
        # who does not have an address.
        return (self.get_account().address is None) & \
               (is_admin(self.request.user.account) | (self.get_account() == self.request.user.account))

    def get_success_url(self):
        return reverse_lazy('account-view', args=[self.get_account().id])

    def form_valid(self, form):
        # We need to do certain things depending on contextually where we came from.
        response = super().form_valid(form)
        # Did we come from account view?
        account = self.get_account()
        account.address = self.object
        account.save()
        return response


class UpdateAddress(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UsAddress
    fields = '__all__'

    def test_func(self):
        return True

    def get_success_url(self):
        return reverse_lazy('account-view', args=[self.get_object().account.id])


class ViewAddress(UserPassesTestMixin, LoginRequiredMixin, DetailView):
    model = UsAddress

    def test_func(self):
        self.request.session['prev_page'] = reverse('address-view', args=[self.request.user.id])
        # We should probably check perms in the template to decide what info is exposed.
        # uh oh! stinky side effects!

        return True

    pass


class CreateAccount(UserPassesTestMixin, View):
    template_name = 'account/create_account.html'

    def get(self, request):
        user = UserCreationForm()

        return render(request,
                      self.template_name, {'user_form': user})

    def post(self, request):
        user = UserCreationForm(request.POST)

        if user.is_valid():
            # we have to process the forms now.
            user.save()

            return redirect('account-view', user.instance.id)
        else:
            return render(request,
                          self.template_name, {'user_form': user})

    def test_func(self):
        return self.request.user.is_anonymous or is_admin(self.request.user.account)


class UpdateAccount(View):
    template_name = 'account/update_account.html'

    def get(self, request, pk):
        user_model = TA_Scheduler.models.User.objects.get(pk=pk)

        user = UserModelForm(instance=user_model)
        account = AccountModelForm(instance=user_model.account)

        return render(request,
                      self.template_name, {'user_form': user, 'account_form': account})

    def post(self, request, pk):
        user_model = TA_Scheduler.models.User.objects.get(pk=pk)

        user = UserModelForm(request.POST, instance=user_model)
        account = AccountModelForm(request.POST, instance=user_model.account)

        if user.is_valid() and account.is_valid():
            # we have to process the forms now.
            user.save()
            account.save()
            # no m2m relationships should be effected here.
            return redirect('account-view', pk=pk)
        else:
            return render(request,
                          self.template_name, {'user_form': user, 'account_form': account})


class ViewAccount(UserPassesTestMixin, LoginRequiredMixin, DetailView):
    model = Account

    def test_func(self):
        # we use this to know what account we need to create an address for.
        self.request.session['account_id_to_change'] = self.get_object().id
        return True


class DeleteAccount(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Account

    def form_valid(self, form):
        self.get_object().user.delete()
        return super().form_valid(form)

    def test_func(self):
        return is_admin(self.request.user.account)

    def get_success_url(self):
        return reverse_lazy('home-page')


class HomeView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'adminHomepage.html'

    def test_func(self):
        return is_admin(self.request.user.account)

    def get(self, request):
        return render(request, self.template_name, {"users": get_all_users(), "courses": Course.objects.all()})

    pass


class CreateCourse(View):
    template_name = 'course/create_course.html'
    model = Course

    def get(self, request):
        course = CourseModelForm()
        return render(request, self.template_name, {'course_form': course})

    def post(self, request):
        course = CourseModelForm(request.POST)

        if course.is_valid():
            course.save()
            return redirect('course-view', course.instance.id)
        else:
            return render(request,
                          self.template_name, {'course_form': course})


class UpdateCourse(View):
    template_name = 'course/update_course.html'

    def get(self, request, pk):
        course_model = TA_Scheduler.models.Course.objects.get(pk=pk)
        course = CourseModelForm(instance=course_model)
        return render(request, self.template_name, {'course_form': course})

    def post(self, request, pk):
        course_model = TA_Scheduler.models.Course.objects.get(pk=pk)
        course = CourseModelForm(request.POST, instance=course_model)

        if course.is_valid():
            course.save()
            return redirect('course-view', pk=pk)
        else:
            return render(request, self.template_name, {'course_form': course})


class ViewCourse(UserPassesTestMixin, LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'course/view_course.html'

    def test_func(self):
        return True

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        course = self.get_object()

        sections = course.section_set.all()

        context = {'course': course, 'sections': sections}
        return render(request, self.template_name, context)


class DeleteCourse(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Course

    def form_valid(self, form):
        self.get_object().delete()
        return super().form_valid(form)

    def test_func(self):
        return is_admin(self.request.user.account)

    def get_success_url(self):
        return reverse_lazy('home-page')


class CreateSection(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'section/create_section.html'
    model = Section

    def get(self, request, pk):
        course = Course.objects.get(id=pk)
        section = SectionModelForm(initial={'course': course}, course=pk)
        return render(request, self.template_name, {'section_form': section})

    def post(self, request, pk):
        course = Course.objects.get(id=pk)
        section = SectionModelForm(pk, request.POST)

        if section.is_valid():
            section = section.save(commit=False)
            section.course = course
            section.save()
            return redirect('section-view', section.id)
        else:
            return render(request, self.template_name, {'section_form': section})

    def get_success_url(self):
        return reverse_lazy('home-page')

    def test_func(self):
        return is_admin(self.request.user.account)


class ViewSection(LoginRequiredMixin, DetailView):
    model = Section

    def test_func(self):
        return True


class UpdateSection(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'section/update_section.html'

    def get(self, request, pk):
        section_model = TA_Scheduler.models.Section.objects.get(pk=pk)
        section = SectionModelForm(section_model.course.id, instance=section_model)
        return render(request, self.template_name, {'section_form': section})

    def post(self, request, pk):
        section_model = TA_Scheduler.models.Section.objects.get(pk=pk)
        section = SectionModelForm(section_model.course.id, request.POST, instance=section_model)

        if section.is_valid():
            section.save()
            return redirect('section-view', pk=pk)
        else:
            return render(request, self.template_name, {'section_form': section})

    def test_func(self):
        return is_admin(self.request.user.account)


class DeleteSection(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Section

    def form_valid(self, form):
        self.get_object().delete()
        return super().form_valid(form)

    def test_func(self):
        return is_admin(self.request.user.account)

    def get_success_url(self):
        return reverse_lazy('course-view', args=self.object.course.id)
