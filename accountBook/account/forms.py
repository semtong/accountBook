from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# 관리자 폼을 커스텀 마이징한다
# 기본폼은 사용하지 않고 추가할 것만 들린다.


class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']