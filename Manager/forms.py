from django import forms
from User.models import AbeUser
from django.contrib.auth.forms import UserCreationForm

class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #htmlの表示を変更可能にします
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].label = 'ユーザー名'
        self.fields['username'].help_text = ''
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].label = 'パスワード'
        self.fields['password1'].help_text = ''
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].label = 'パスワード(確認)'
        self.fields['password2'].help_text = '上のパスワードと同じものを入力してください'

    class Meta:
       model = AbeUser
       fields = ("username", "password1", "password2",)

class DeleteUserSelectForm(forms.Form):
    users = forms.ChoiceField(widget=forms.widgets.Select(attrs={'class': 'form-control'}), label='削除するユーザー', choices=[(x.pk, x.username) for x in AbeUser.objects.filter(is_staff=False)])