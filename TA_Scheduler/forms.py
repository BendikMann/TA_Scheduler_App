from django import forms


class EmailForm(forms.Form):
    header = forms.CharField(label='header')
    content = forms.CharField(label='content')
