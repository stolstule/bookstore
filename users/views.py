import sys
sys.path.append("..store")
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from store.models import Book, Category
from .models import Basket
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy

hud_genre_navbar = Category.objects.filter(section='Художественная литература')
nehud_genre_navbar = Category.objects.filter(section='Нехудожественная литература')

def register(request):
    field_errors = ''
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid() and not User.objects.filter(email=form.data['email']):
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Профиль создан')
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

        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, f'Ваш профиль обновлен')
            return redirect('profile')

        if user_form.is_valid():
            user_form.save()
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

class PasswordChange(PasswordChangeView):
    template_name = 'password_change.html'
    success_url = 'users/pass_change_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hud_genre_navbar'] = hud_genre_navbar
        context['nehud_genre_navbar'] = nehud_genre_navbar
        return context

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        errors_list = []
        for error in form.errors.values():
            if 'The two password fields didn’t match.' in error:
                errors_list.append('Пароли не совпадают.')
            if 'Your old password was entered incorrectly. Please enter it again.' in error:
                errors_list.append('Ваш старый пароль неверен.')
        context['errors_list'] = errors_list
        return self.render_to_response(context)


class UserForgotPasswordView(SuccessMessageMixin, PasswordResetView):

    template_name = 'users/password_recovery.html'
    success_url = reverse_lazy('login')
    success_message = 'Письмо с инструкцией по восстановлению пароля отправлено на ваш email'
    subject_template_name = 'users/email/pass_subject_mail.txt'
    email_template_name = 'users/email/pass_recovery_mail.html'

    def form_valid(self, form):
        if User.objects.filter(email=form.data['email']):
            return super().form_valid(form)
        else:
            return super().form_invalid(form)
    def form_invalid(self, form):
        messages.error(self.request, 'Такой почты не существует')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Сброс пароля на сайте'
        context['hud_genre_navbar'] = hud_genre_navbar
        context['nehud_genre_navbar'] = nehud_genre_navbar
        return context


class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):

    template_name = 'users/set_new_pass.html'
    success_url = reverse_lazy('login')
    success_message = 'Пароль успешно изменен'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Установить новый пароль'
        context['hud_genre_navbar'] = hud_genre_navbar
        context['nehud_genre_navbar'] = nehud_genre_navbar
        return context


def basket_page(request):
    if request.user.is_authenticated:
        total_sum = 0
        baskets = []
        for item in Basket.objects.filter(user=request.user):
            baskets.append(item.book)
            total_sum += item.book.price
        return render(request, 'users/basket.html', {
            'baskets': baskets,
            'total_sum': total_sum,
            'hud_genre_navbar': hud_genre_navbar,
            'nehud_genre_navbar': nehud_genre_navbar
        })
    else:
        total_sum = 0
        baskets = []
        if len(request.session.keys()) != 0:
            for book_id in request.session['basket']:
                baskets.append(Book.objects.get(id=book_id))
                total_sum += Book.objects.get(id=book_id).price
        else:
            request.session['basket'] = []

        return render(request, 'users/basket.html', {
            'baskets': baskets,
            'total_sum': total_sum,
            'hud_genre_navbar': hud_genre_navbar,
            'nehud_genre_navbar': nehud_genre_navbar
        })


def basket_add(request, book_id):
    if request.user.is_authenticated:
        book = Book.objects.get(id=book_id)
        baskets = Basket.objects.filter(user=request.user, book=book)
        if not baskets.exists():
            Basket.objects.create(user=request.user, book=book)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        if len(request.session.keys()) != 0:
            book_list = request.session['basket']
            book_list.append(book_id)
        else:
            book_list = [book_id]
            request.session['basket'] = book_list
        request.session['basket'] = book_list
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


def book_remove(request, book_id):
    if request.user.is_authenticated:
        book = Basket.objects.get(user=request.user, book_id=book_id)
        book.delete()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        basket = request.session['basket']
        basket.remove(book_id)
        request.session['basket'] = basket
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


def basket_remove(request):
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
        basket.delete()
    else:
        request.session['basket'] = []
    return HttpResponseRedirect(request.META['HTTP_REFERER'])