import sys
sys.path.append("..users")
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from store.models import Book, Category
from .forms import UserRegisterForm

hud_genre_navbar = Category.objects.filter(section='Художественная литература')
nehud_genre_navbar = Category.objects.filter(section='Нехудожественная литература')

class Register(View):
	def get(self, request):
		form = UserRegisterForm()
		return render(request, 'users/register_page.html', {
			'form': form,
			'hud_genre_navbar': hud_genre_navbar,
			'nehud_genre_navbar': nehud_genre_navbar
		})

	def post(self, request):
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Создан аккаунт {username}!')
			return redirect('blog-home')
		return render(request, 'users/register_page.html', {
			'form': form,
			'hud_genre_navbar': hud_genre_navbar,
			'nehud_genre_navbar': nehud_genre_navbar
		})