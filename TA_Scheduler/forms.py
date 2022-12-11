from django.contrib.auth.forms import UserCreationForm
from django import forms

import TA_Scheduler.models


class NewUserCreationForm(UserCreationForm):
    class Meta:
        model = TA_Scheduler.models.User
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']

        widgets = {
            # Keep this here for alex, so he can do his styling.
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # I'm not quite sure why Django needs it this way, but to access these two fields
        # We need to access them specifically like this. Other methods I tried actually
        # made it seem as if these fields did not exist (but it does) ¯\_(ツ)_/¯
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'


