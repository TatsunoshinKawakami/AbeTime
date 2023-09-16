from django import forms
from .models import Log, AbeUser
from Manager.models import WellKnownLocation
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UsernameField,
)
from django.utils import timezone

state_choices = [("0", "◯"), ("1", "△"), ("2", "✕")]

class LogForm(forms.Form):
    state = forms.ChoiceField(widget=forms.widgets.RadioSelect, choices=state_choices)
    well_known_location = forms.ChoiceField(widget=forms.widgets.Select(attrs={"class": "form-control"}),label="現場名")
    location = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['well_known_location'].choices = [(location.id, location.location_name) for location in WellKnownLocation.objects.all().order_by('deletibility')]


class DateSelectForm(forms.Form):
    year = forms.ChoiceField(widget=forms.widgets.Select(attrs={"class": "form-control"}))
    month = forms.ChoiceField(widget=forms.widgets.Select(attrs={"class": "form-control"}))
    day = forms.ChoiceField(widget=forms.widgets.Select(attrs={"class": "form-control"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['year'].choices = [
            (y, str(y) + "年")
            for y in range(timezone.now().year - 5, timezone.now().year + 1)
        ]
        self.fields['year'].initial = timezone.now().year

        self.fields['month'].choices = [(m, str(m) + "月") for m in range(1, 13)]
        self.fields['month'].initial = timezone.now().month

        self.fields['day'].choices = [(d, str(d) + "日") for d in range(1, 32)]
        self.fields['day'].initial = timezone.now().day


class LoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={"autofocus": True, "class": "form-control"}),
        label="ユーザー名",
    )
    password = forms.CharField(
        label=("パスワード"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "class": "form-control"}
        ),
    )

    error_messages = {
        "invalid_login": ("ユーザー名、またはパスワードが間違っています"),
        "inactive": ("このアカウントは使用できません"),
    }
