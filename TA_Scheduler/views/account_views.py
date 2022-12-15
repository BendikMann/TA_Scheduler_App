from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from TA_Scheduler.user import make_admin, make_ta, make_instructor
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView

from TA_Scheduler.forms import NewUserCreationForm
from TA_Scheduler.models import UsAddress, User, UserModelForm
from TA_Scheduler.user import is_admin


class CreateAddress(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = UsAddress
    fields = '__all__'

    def get_account(self) -> User:
        try:
            account_id = int(self.request.session.get('account_id_to_change'))
        except TypeError:
            raise PermissionDenied()
        user = User.objects.get(id=account_id)
        return user

    def test_func(self):
        # User to create address for does not have an address and the one creating the address is an admin or the user
        # who does not have an address.
        return (self.get_account().address is None) & \
               (is_admin(self.request.user) | (self.get_account() == self.request.user))

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
        return reverse_lazy('account-view', args=[self.get_object().user.id])


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
        user = NewUserCreationForm()

        return render(request,
                      self.template_name, {'user_form': user})

    def post(self, request):
        user = NewUserCreationForm(request.POST)

        if user.is_valid():
            # we have to process the forms now.
            user.save()
            # check the selected group and call the appropriate method
            selected_group = request.POST.get("group")
            if selected_group == "Admin":
                make_admin(user.instance)
            elif selected_group == "Instructor":
                make_instructor(user.instance)
            elif selected_group == "TA":
                make_ta(user.instance)

            return redirect('account-view', user.instance.id)
        else:
            return render(request,
                          self.template_name, {'user_form': user})

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        return self.request.user.is_anonymous or is_admin(self.request.user)


class UpdateAccount(View):
    template_name = 'account/update_account.html'

    def get(self, request, pk):
        user_model = User.objects.get(pk=pk)

        user = UserModelForm(instance=user_model)

        return render(request,
                      self.template_name, {'user_form': user})

    def post(self, request, pk):
        user_model = User.objects.get(pk=pk)

        user = UserModelForm(request.POST, instance=user_model)

        if user.is_valid():
            # we have to process the forms now.
            user.save()
            # no m2m relationships should be effected here.
            return redirect('account-view', pk=pk)
        else:
            return render(request,
                          self.template_name, {'user_form': user})


class ViewAccount(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = User

    def test_func(self):
        # we use this to know what account we need to create an address for.
        self.request.session['account_id_to_change'] = self.get_object().id
        return True


class DeleteAccount(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User

    def form_valid(self, form):
        self.get_object().delete()
        return super().form_valid(form)

    def test_func(self):
        return is_admin(self.request.user)

    def get_success_url(self):
        return reverse_lazy('home-page')
