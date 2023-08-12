from django import forms
from .models import Log, AbeUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

choices = {('0', '◯'), ('1', '△'), ('2', '✕')}

class LogForm(forms.Form):
    state = forms.ChoiceField(widget=forms.widgets.RadioSelect, choices=choices)
    location = forms.CharField(required=False)

class SignupForm(UserCreationForm):
    class Meta:
        model = AbeUser
        fields = ['username', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    pass