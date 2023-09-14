from django import forms
from .models import Log, AbeUser
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UsernameField,
)
from django.utils import timezone

state_choices = [("0", "◯"), ("1", "△"), ("2", "✕")]
location_choices = [
    ("0", "---"),
    ("1", "津田建築"),
    ("2", "ヤマタホーム"),
    ("3", "笹間建材"),
    ("4", "松本油店"),
    ("5", "Bクランプ"),
    ("6", "多林製作所"),
    ("7", "湯村工匠"),
    ("8", "ビルフィール"),
    ("9", "西尾建設"),
    ("10", "その他"),
]


class LogForm(forms.Form):
    state = forms.ChoiceField(widget=forms.widgets.RadioSelect, choices=state_choices)
    well_known_location = forms.ChoiceField(
        widget=forms.widgets.Select(attrs={"class": "form-control"}),
        label="現場名",
        choices=location_choices,
        initial=["0"],
    )
    location = forms.CharField(required=False)


class DateSelectForm(forms.Form):
    year = forms.ChoiceField(
        widget=forms.widgets.Select(attrs={"class": "form-control"}),
        choices=[
            (y, str(y) + "年")
            for y in range(timezone.now().year - 5, timezone.now().year + 1)
        ],
        initial=timezone.now().year,
    )
    month = forms.ChoiceField(
        widget=forms.widgets.Select(attrs={"class": "form-control"}),
        choices=[(m, str(m) + "月") for m in range(1, 13)],
        initial=timezone.now().month,
    )
    day = forms.ChoiceField(
        widget=forms.widgets.Select(attrs={"class": "form-control"}),
        choices=[(d, str(d) + "日") for d in range(1, 32)],
        initial=timezone.now().day,
    )


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
