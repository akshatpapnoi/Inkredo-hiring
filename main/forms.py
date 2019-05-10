from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Company

class DateInput(forms.DateInput):
    input_type = 'date'


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

class UserProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(required = False, widget = DateInput())

    class Meta:
        model = UserProfile
        exclude = ['user']

class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        exclude = ['admin']