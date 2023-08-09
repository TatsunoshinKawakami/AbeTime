from django import forms
from .models import Log, AbeUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class LogForm(forms.ModelForm):
    class Meta:
        model = Log
        fields = ['state', 'location']

class SignupForm(UserCreationForm):
    class Meta:
        model = AbeUser
        fields = ['username', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    pass