from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, DeleteView

from TA_Scheduler.models import Course, CourseModelForm
from TA_Scheduler.user import is_admin


class CreateCourse(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'course/create_course.html'
    model = Course

    def test_func(self):
        return is_admin(self.request.user)

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


class UpdateCourse(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'course/update_course.html'

    def test_func(self):
        return is_admin(self.request.user)

    def get(self, request, pk):
        course_model = Course.objects.get(pk=pk)
        course = CourseModelForm(instance=course_model)
        return render(request, self.template_name, {'course_form': course})

    def post(self, request, pk):
        course_model = Course.objects.get(pk=pk)
        course = CourseModelForm(request.POST, instance=course_model)

        if course.is_valid():
            course.save()
            return redirect('course-view', pk=pk)
        else:
            return render(request, self.template_name, {'course_form': course})


class ViewCourse(LoginRequiredMixin, DetailView):
    model = Course

class DeleteCourse(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model = Course

    def form_valid(self, form):
        self.get_object().delete()
        return super().form_valid(form)

    def test_func(self):
        return is_admin(self.request.user)
        # return True

    def get_success_url(self):
        return reverse_lazy('home-page')
