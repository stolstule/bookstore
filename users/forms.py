from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.forms import ModelForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    error_messages = {
        'password_mismatch': "Пароли не совпадают!",
    }
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        error_messages = {
            'username': {
                'unique': 'Такое имя уже существует!',
            },
        }

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['image']