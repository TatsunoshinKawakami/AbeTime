from django import forms
from .models import Log, AbeUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils import timezone

choices = [('0', '◯'), ('1', '△'), ('2', '✕')]

class LogForm(forms.Form):
    state = forms.ChoiceField(widget=forms.widgets.RadioSelect, choices=choices)
    location = forms.CharField(required=False)

class DateSelectForm(forms.Form):
    year = forms.ChoiceField(widget=forms.widgets.Select(attrs={'class': 'form-control'}), choices=[(y, str(y)+'年') for y in range(timezone.now().year-5, timezone.now().year+1)], initial=timezone.now().year)
    month = forms.ChoiceField(widget=forms.widgets.Select(attrs={'class': 'form-control'}), choices=[(m, str(m)+'月') for m in range(1, 13)], initial=timezone.now().month)
    day = forms.ChoiceField(widget=forms.widgets.Select(attrs={'class': 'form-control'}), choices=[(d, str(d)+'日') for d in range(1, 32)], initial=timezone.now().day)

class SignupForm(UserCreationForm):
    class Meta:
        model = AbeUser
        fields = ['username', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    pass