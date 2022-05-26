from django import forms
from django.forms import ModelForm
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

class SignupForm(UserCreationForm): # 내장 회원가입 폼을 상속받아서 확장한다.
    class Meta:
        model = CustomUser
        fields = ["email","birth_year","u_sex","u_nickname","username","login_method"]

class Signup_manager(UserCreationForm): # 내장 회원가입 폼을 상속받아서 확장한다.
    class Meta:
        model = CustomUser
        fields = ["email","birth_year","u_sex","u_nickname","username","login_method","is_manager","is_master"]

# class UserChangeForm(forms):
#     # password = ReadOnlyPasswordHashField()
#     class Meta:
#         fields = ['u_nickname']

    # def clean_password(self):
    #     return self.initial["password"]

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['u_nickname','email','u_sex','birth_year']


class UpdateProfileForm(forms.ModelForm):
    u_nickname = forms.CharField()
    email = forms.CharField()
    u_sex = forms.CharField()
    birth_year = forms.CharField()
    class Meta:
        model = CustomUser
        fields = ['u_nickname','email','u_sex','birth_year']


class CheckPasswordForm(forms.Form):
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput(
        attrs={'class': 'form-control', }),
                               )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = self.user.password

        if password:
            if not check_password(password, confirm_password):
                self.add_error('password', '비밀번호가 일치하지 않습니다.')