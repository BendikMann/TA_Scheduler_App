from django import forms
from TA_Scheduler.models import *


class UserModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'myfieldclass'}),
            'last_name': forms.TextInput(attrs={'class': 'myfieldclass'}),
        }
