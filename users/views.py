import sys
sys.path.append("..store")
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from store.models import Book, Category
from .forms import UserRegisterForm, UserAuthenticationForm

hud_genre_navbar = Category.objects.filter(section='Художественная литература')
nehud_genre_navbar = Category.objects.filter(section='Нехудожественная литература')

def register(request):
	field_errors = ''
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid() and  not User.objects.filter(email=form.data['email']):
			form.save()
			username = form.cleaned_data.get('username')
			return redirect('/')
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


def login_views(request):
    error = ''
    if request.method == 'POST':
        form = UserAuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request=request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('/')
        else:
            error = 'Вы ввели неправильный логин или пароль!'
    else:
        form = UserAuthenticationForm()
    return render(request, 'users/login.html', {
        'form': form,
        'field_error': error
    })

@login_required
def profile(request):
    return render(request, 'users/profile.html')