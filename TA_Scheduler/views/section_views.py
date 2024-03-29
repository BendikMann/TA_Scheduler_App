import TA_Scheduler.models
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView

from django.views.generic.edit import CreateView, DeleteView, UpdateView

from TA_Scheduler.models import *
from TA_Scheduler.user import *


class CreateSection(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'section/create_section.html'
    model = Section

    def get(self, request, pk):
        course = Course.objects.get(id=pk)
        section = SectionModelForm(initial={'course': course})
        return render(request, self.template_name, {'section_form': section})

    def post(self, request, pk):
        course = Course.objects.get(id=pk)
        section = SectionModelForm(request.POST)

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
        return is_admin(self.request.user)


class ViewSection(LoginRequiredMixin, DetailView):
    model = Section


class UpdateSection(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'section/update_section.html'

    def get(self, request, pk):
        section_model = TA_Scheduler.models.Section.objects.get(pk=pk)
        section = SectionModelForm(instance=section_model)
        return render(request, self.template_name, {'section_form': section})

    def post(self, request, pk):
        section_model = TA_Scheduler.models.Section.objects.get(pk=pk)
        section = SectionModelForm(request.POST, instance=section_model)

        if section.is_valid():
            # its hard to clear it in the right conditions so we clear assigned user if type of section changes.
            if 'type' in section.changed_data:
                section_model.assigned_user = None
            section.save()
            return redirect('section-view', pk=pk)
        else:
            return render(request, self.template_name, {'section_form': section})

    def test_func(self):
        return is_admin(self.request.user)


class AssignSection(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'section/assign_section.html'

    def get(self, request, pk):
        section = AssignSectionModelForm(instance=Section.objects.get(pk=pk))
        section_data = Section.objects.get(pk=pk)
        return render(request, self.template_name, {'section_form': section, 'section_data': section_data})

    def post(self, request, pk):
        section = AssignSectionModelForm(request.POST, instance=Section.objects.get(pk=pk))
        if section.is_valid():
            section.save()
            return redirect('section-view', pk=pk)
        else:
            return render(request, self.template_name, {'section_form': section})

    def test_func(self):
        return is_admin(self.request.user) or is_instructor(self.request.user)


class DeleteSection(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Section

    def form_valid(self, form):
        self.get_object().delete()
        return super().form_valid(form)

    def test_func(self):
        return is_admin(self.request.user)

    def get_success_url(self):
        return reverse_lazy('course-view', args=(self.object.course.id,))
