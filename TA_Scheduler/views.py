from django.core.exceptions import PermissionDenied

import TA_Scheduler.models
import django.contrib.auth.models
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView

from django.views.generic.edit import CreateView, DeleteView, UpdateView
from TA_Scheduler.models import *
from TA_Scheduler.user import is_admin


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


class HomeView(View):
    template_name = 'adminHomepage.html'

    def get(self, request):
        return render(request, self.template_name)

    pass
