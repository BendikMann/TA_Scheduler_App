from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView

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
