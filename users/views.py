import sys
sys.path.append("..store")
from django.contrib.auth import authenticate, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from store.models import Book, Category
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

hud_genre_navbar = Category.objects.filter(section='Художественная литература')
nehud_genre_navbar = Category.objects.filter(section='Нехудожественная литература')

def register(request):
	field_errors = ''
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid() and  not User.objects.filter(email=form.data['email']):
			form.save()
			username = form.cleaned_data.get('username')
			return redirect('login')
		elif form.errors:
			field_errors = []
			if User.objects.filter(email=form.data['email']):
				field_errors.append('Такой email уже используется!')
			for value_list in form.errors.values():
				for value in value_list:
					if value == 'This password is too short. It must contain at least 8 characters.':
						field_errors.append('Пароль должен содержать не менее 8 символов!')
					elif value == 'This password is too common.':
						field_errors.append('Этот пароль слишком простой, пароль должен содержать цифры, заглавные и строчные буквы!')
					elif value == 'The password is too similar to the username.':
						field_errors.append('Пароль слишком похож на логин!')
					else:
						field_errors.append(value)
	else:
		form = UserRegisterForm()
	return render(request, 'users/register_page.html', {
		'form': form,
		'field_errors': field_errors,
		'hud_genre_navbar': hud_genre_navbar,
		'nehud_genre_navbar': nehud_genre_navbar
	})

class LoginPage(LoginView):
    template_name = 'users/login.html'
    error_messages = {
		'invalid_login': 'Вы ввели неправильный логин или пароль!',
		'inactive': 'Вы ввели неправильный логин или пароль!'
	}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hud_genre_navbar'] = hud_genre_navbar
        context['nehud_genre_navbar'] = nehud_genre_navbar
        return context

def logout_view(request):
    logout(request)
    return render(request, 'users/logout.html', {
		'hud_genre_navbar': hud_genre_navbar,
		'nehud_genre_navbar': nehud_genre_navbar
	})

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Ваш профиль обновлен')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {
        'hud_genre_navbar': hud_genre_navbar,
        'nehud_genre_navbar': nehud_genre_navbar,
		'user_form': user_form,
		'profile_form': profile_form
    })