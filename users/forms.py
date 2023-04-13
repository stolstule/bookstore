from django import forms
from django.forms import TextInput, EmailInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


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

class UserAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': 'Вы ввели неправильный логин или пароль!',
        'inactive': 'Это аккаунт не активен!'
    }